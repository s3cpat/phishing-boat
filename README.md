# phishing-boat - *a phishing email analysis container*

## Screenshots

![Upload Page](screenshots/Screenshot_2018-11-25%20Upload%20Phishing%20Boat.png)
![Analysis Pagae](screenshots/Screenshot_2018-11-25%20Analysis%20f_r_e_e_v_b_u_c_k_s%20eml%20Phishing%20Boat.png)

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