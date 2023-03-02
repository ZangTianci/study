int serialOpen (const char *device, const int baud);
void serialSendStr (const int fd, const char *s);
int serialGetStr (const int fd, char *buffer);
