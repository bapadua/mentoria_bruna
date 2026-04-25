import urllib.request

url = "https://SEU-BUCKET.s3.amazonaws.com/transacoes.csv"
response = urllib.request.urlopen(url)
data = response.read().decode('utf-8')
lines = data.split('\n')
for i in range(5):
    print(lines[i])