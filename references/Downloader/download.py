import sys
import requests

# link = "https://mirror.kakao.com/ubuntu-releases/20.04.2.0/ubuntu-20.04.2.0-desktop-amd64.iso"
link = 'http://112.151.179.200:25565/2021%2d04%2d24%2022%2d44%2d33.mkv'
file_name = "download.iso"
with open(file_name, "wb") as f:
    print("Downloading %s" % file_name)
    response = requests.get(link, stream=True)
    total_length = response.headers.get('content-length')
    name = response.headers.get('content-disposition')
    print(name)

    if total_length is None: # no content length header
        f.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)

            done = int(100 * dl / total_length)

            sys.stdout.write('\r{}%'.format(str(done).zfill(3)))
            sys.stdout.flush()