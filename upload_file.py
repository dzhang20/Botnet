import os, sys, requests

#Upload file 
def upload(host, port, filepath):
    url = "http://"+host+":"+str(port)
    fp = open(filepath, 'rb')
    files = {'file':fp}
    r = requests.post(url, files=files)

    fp.close()

#useage: python upload.py [host] [port] [filepath]
def main():
    if len(sys.argv) != 4:
        sys.exit(1)
    host = sys.argv[1]
    port = int(sys.argv[2])
    filepath = sys.argv[3]
    upload(host, port, filepath)

if __name__ == '__main__':
    main()
