import multiprocessing
import requests

def worker(threadname, name, url, filename):
    file_name = filename
    with open(file_name, "wb") as f:
        # print("Downloading %s" % file_name)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            ddone = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)

                done = int(100 * dl / total_length)
                # if ddone != done:
                    # if threadname == '1':
                        # print('{} : {}'.format(threadname, done))
                    # else:
                        # print('\t{} : {}'.format(threadname, done))
                ddone = done

# Mind the "if" instruction!
if __name__ == '__main__':
    global link
    jobs = []
    while True:
        th = input('thread namae : ')
        name = input('name : ')
        url = input('url : ')
        filename = input('filenamae : ')
        p = multiprocessing.Process(target=worker, args=(th, name, url, filename, )).start()