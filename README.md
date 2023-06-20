# Controly

V tem README bom predstavil aplikacijo Controly

## 1. Kaj je to?
Controly je spletna aplikacija, na kateri lahko preprosto upravljaš s 'Controly Napravo'. Projekt je sestavljen iz dveh delov, spletne aplikacije za nadzor nad napravami in fizične naprave.

**Fizična naprava** je enota sestavljena iz Arduino mikrokrmilnika in Raspberry Pi računalnika. Raspberry Pi je uporabljen za povezavo Arduina s glavnim Controly strežnikom in zagotavlja prenos podatkov med spletno aplikacijo in Arduinom

**Spletna aplikacija:**
![Spletna aplikacija](https://i.postimg.cc/NFNK8Y6X/Screenshot-2023-06-20-at-13-39-01.png)
Uporabnik lahko preprosto spreminja/nadzoruje želeno napravo in njene lastnosti
Ko uporabnik shrani spremembe na spletni strani se zamenja tudi lastnost na izbrani napravi.
**Primer:** Uporabnik upravlja z Controly napravo 'Stopnice' (po naših stopnicah so nameščene LED lučke. Vsakič, ko gre nekdo po stopnicah gor, se lučke prižgejo). Uporabnik je na spletni strani izbral zeleno barvo. Ko gre nekdo gor, se prižgejo zeleno.
![enter image description here](https://i.postimg.cc/7htXb5LJ/IMG-2605.png)
![enter image description here](https://i.postimg.cc/yYWvtyfm/IMG-2606.png)

## 2. Prednosti
### 1. Izjemna odzivnost platforme - od klika gumba 'Shrani' na spletu in vse do dejanske spremembe naprave traja v povprečju ±0.5 sekund
### 2. Obojestransko pošiljanje informacij - Controly naprava lahko pošlje informacije nazaj spletni aplikaciji (npr.: 'uspešna naložitev', 'zaznano gibanje',...)

## Slike
Delovanje aplikacije se še najlažje prikaže s slikami

### Prijava
![Prijava](https://i.postimg.cc/Y9gtd7QV/Screenshot-2023-06-20-at-13-34-30.png)

### Nadzor nad napravami
![Nadzor](https://i.postimg.cc/8kt0x3wn/Screenshot-2023-06-20-at-13-35-18.png)

### Dodajanje naprave - ko dodaš napravo se samodejno prenese potrebna C++ koda za upravljanje z mikrokrmilnikom
![Prenos](https://i.postimg.cc/s2HmDB0F/Screenshot-2023-06-20-at-13-54-26.png)
