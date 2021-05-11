import urllib3 as u3
import urllib.request as ur
from bs4 import BeautifulSoup as bs
import sys

http = u3.PoolManager()

def GrabHTML(url):
    page = http.request('GET', url)
    return page.data.decode('utf-8')

base = 'https://www.pokemon.com'

pokemon = []

descriptions = []

height = []

weight = []

number = []

img = []

firstPokemon = "Bulbasaur"

nextName = firstPokemon

nextURL = f'/us/pokedex/{firstPokemon}'

running = True

while(running):
    pokemon.append(nextName)

    save = GrabHTML(f"{base}{nextURL}")
    save = bs(save, "html.parser")

    # get pokemon pokedex number
    allN = save.findAll("span", {"class": "pokemon-number"})

    number.append(int(allN[2].text[1:]))

    print(str(number[-1:][0]) + ' ' + nextName)

    # get pokemon's image
    if(number[-1:][0] < 10):
        img.append(f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/00{number[-1:][0]}.png")
    elif(number[-1:][0] >= 10 and number[-1:][0] < 100):
        img.append(f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/0{number[-1:][0]}.png")
    else:
        img.append(f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{number[-1:][0]}.png")
    # ***WILL HAVE TO CHANGE IF NUMBER OF POKEMON REACHES OVER 1000 ***

    # get height and weight
    details = save.findAll("span", {"class": "attribute-value"})

    height.append(details[0].text)
    weight.append(details[1].text.split(' ')[0])

    # get next pokemon url
    nextURL = str(save.find("a", {"class": "next"}, href=True)).split('"')[3]

    # get next pokemon name
    nextName = save.findAll("span", {"class": "pokemon-name hidden-mobile"})[1].text

    # break if we arrive back at first pokemon
    running = False if nextName == firstPokemon else True

    # get x-version description
    save = save.find("p", {"class": "version-x"}).text[19:].replace('\n',' ')

    descriptions.append(save)

print("saving data to tsv...")
with open(f"pokemon.tsv", 'w', encoding='utf8') as f:
    ret = 'index\tname\theight\tweight\tdescription\timage'

    for i in range(len(descriptions)):
        ret += (f"\n{number[i]}\t{pokemon[i]}\t{height[i]}\t{weight[i]}\t{descriptions[i]}\t{img[i]}")

    f.write(ret)