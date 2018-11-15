# phishing-boat - *a phishing email analysis container*

## Installation and Running

```bash
docker build -t phishing-boat .
docker run -it -d --rm -p 80:80 --name sailing phishing-boat
# open localhost/ in your favorite browser
#  and upload an .eml/.msg for analysis
```