/*
 * gdb_mcp_compat.c - GDB wrapper for MCP compatibility
 *
 * Replaces "^connected\r\n" with "^done\r\n" in GDB's stdout,
 * so that GDB MCP's gdb_connect() can recognize successful remote connections.
 *
 * Usage: gdb_mcp_compat.exe [gdb_args...]
 */
#include <windows.h>
#include <stdio.h>
#include <string.h>

static FILE *g_log = NULL;

static void log_open(void) {
    g_log = fopen("C:\\Temp\\wrapper_debug.log", "w");
    if (!g_log) g_log = fopen("E:\\wrapper_debug.log", "w");
}
static void log_msg(const char *msg) {
    if (g_log) { fputs(msg, g_log); fflush(g_log); }
}
static void log_hex(const char *label, const char *buf, int len) {
    if (!g_log) return;
    fprintf(g_log, "%s [%d bytes]: ", label, len);
    for (int i = 0; i < len && i < 64; i++) fprintf(g_log, "%02X ", (unsigned char)buf[i]);
    fputs("\n", g_log);
    fflush(g_log);
}

#define GDB_PATH "E:\\Workspace\\yugioh-ex2006-re\\tools\\arm-none-eabi-gdb.exe"
#define BUF_SIZE 4096

/* Pattern to detect and replace (GDB on Windows emits CRLF) */
static const char *NEEDLE = "^connected\r\n";
static const char *REPLACE = "^done\r\n";

/*
 * State machine that reads from hIn byte-by-byte,
 * buffers possible needle match, and writes filtered output to hOut.
 */
static void pump_and_filter(HANDLE hIn, HANDLE hOut) {
    int needle_len = (int)strlen(NEEDLE);
    int replace_len = (int)strlen(REPLACE);
    char match_buf[16]; /* must be >= needle_len */
    int match_pos = 0;  /* how many needle chars we've tentatively matched */

    char byte;
    DWORD nr, nw;

    while (ReadFile(hIn, &byte, 1, &nr, NULL) && nr > 0) {
        char hex[8]; sprintf(hex, "%02X ", (unsigned char)byte); log_msg(hex);
        if (byte == NEEDLE[match_pos]) {
            /* Continues current match attempt */
            match_buf[match_pos++] = byte;
            if (match_pos == needle_len) {
                /* Full match: emit replacement */
                log_msg("\n[WRAPPER] REPLACING ^connected\\r\\n -> ^done\\r\\n\n");
                WriteFile(hOut, REPLACE, replace_len, &nw, NULL);
                match_pos = 0;
            }
        } else {
            /* No match: flush buffered partial match then this byte */
            if (match_pos > 0) {
                WriteFile(hOut, match_buf, match_pos, &nw, NULL);
                match_pos = 0;
                /* Re-check current byte against fresh needle start */
                if (byte == NEEDLE[0]) {
                    match_buf[match_pos++] = byte;
                } else {
                    WriteFile(hOut, &byte, 1, &nw, NULL);
                }
            } else {
                WriteFile(hOut, &byte, 1, &nw, NULL);
            }
        }
    }
    /* Flush remaining partial match */
    if (match_pos > 0) {
        WriteFile(hOut, match_buf, match_pos, &nw, NULL);
    }
}

int main(int argc, char *argv[]) {
    log_open();
    log_msg("[WRAPPER] Started\n");
    /* Log all arguments */
    for (int i = 0; i < argc; i++) {
        char buf[512];
        snprintf(buf, sizeof(buf), "[WRAPPER] argv[%d] = %s\n", i, argv[i]);
        log_msg(buf);
    }
    /* Build command line */
    char cmdline[8192];
    int pos = 0;
    pos += snprintf(cmdline + pos, sizeof(cmdline) - pos, "\"%s\"", GDB_PATH);
    for (int i = 1; i < argc; i++) {
        pos += snprintf(cmdline + pos, sizeof(cmdline) - pos, " %s", argv[i]);
    }

    SECURITY_ATTRIBUTES sa = {sizeof(sa), NULL, TRUE};
    HANDLE hReadOut, hWriteOut;
    if (!CreatePipe(&hReadOut, &hWriteOut, &sa, 0)) return 1;
    SetHandleInformation(hReadOut, HANDLE_FLAG_INHERIT, 0);

    STARTUPINFOA si = {sizeof(si)};
    si.dwFlags = STARTF_USESTDHANDLES;
    si.hStdInput  = GetStdHandle(STD_INPUT_HANDLE);
    si.hStdOutput = hWriteOut;
    si.hStdError  = GetStdHandle(STD_ERROR_HANDLE);

    PROCESS_INFORMATION pi;
    if (!CreateProcessA(NULL, cmdline, NULL, NULL, TRUE, 0, NULL, NULL, &si, &pi)) {
        log_msg("[WRAPPER] Failed to start GDB\n");
        fprintf(stderr, "Failed to start GDB: %lu\n", GetLastError());
        return 1;
    }
    log_msg("[WRAPPER] GDB started\n");
    CloseHandle(hWriteOut);

    pump_and_filter(hReadOut, GetStdHandle(STD_OUTPUT_HANDLE));

    WaitForSingleObject(pi.hProcess, INFINITE);
    DWORD exitCode = 0;
    GetExitCodeProcess(pi.hProcess, &exitCode);
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    CloseHandle(hReadOut);
    return (int)exitCode;
}
