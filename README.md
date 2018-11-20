# phishing-boat - *a phishing email analysis container*

## Installation and Running

```bash
docker build -t phishing-boat .
docker run -it -d -e VT_API_KEY=<keyhere> --rm -p 80:80 --mount src=vol2,dst=/usr/src/app/uploads --name sailing phishing-boat
# open localhost/ in your favorite browser
#  and upload an .eml/.msg for analysis
# remove --mount option (with src,dst) to remove persistence
# -e VT_API_KEY=<keyhere> is for public api
# -e VT_PRIV_API_KEY=<keyhere> is for private api
```