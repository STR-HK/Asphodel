import threading
import requests

def task1(link, file_name):
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')
        name = response.headers.get('content-disposition')
        print(name)

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
                if ddone != done:
                    print('task1 : {}'.format(done))
                ddone = done

link = 'http://112.151.179.200:25565/2021%2d04%2d24%2022%2d44%2d33.mkv'
file_name = "download1.mkv"
task1 = threading.Thread(target=task1, args=(link, file_name))

link = 'https://mirror.kakao.com/ubuntu-releases/20.04.2.0/ubuntu-20.04.2.0-desktop-amd64.iso'
file_name = "download2.iso"
task2 = threading.Thread(target=task1, args=(link, file_name))

if __name__ == "__main__":
    print("START")
    task1.start()
    task2.start()
    
    task1.join()
    task2.join()
    print("END")