# -*- coding: utf-8 -*-
"""
Created on Fri May 18 11:07:05 2018

@author: Dell
"""

from PIL import Image
import random
import plotly.graph_objs as go
import plotly.offline as offline


#funkcja szyfrujaca

def encoder(image_location):
    
    image = Image.open(image_location)
    message = input('Podaj wiadomosc do zakodowania (bez polskich znakow): ')
    
    #przeksztalcenie podanej wiadomosci na strumien bitow (kodowanie ASCII).
    #7 zer oznacza koniec wiadmosci.
    #kolejne bity generowane sa losowo.
    
    bitstream = ""
    for ch in message:
        char = format(ord(ch), '07b')
        bitstream += char 
    bitstream += "0000000"
    for n in range(image.height*image.width*3):
        bitstream += str(random.randint(0, 1))
        
    bit = iter(bitstream)
    
    #zapisanie nowego obrazu podmieniajac najmniej znaczace bity. 
    #modyfikowane sa kolejne piksele poczynajac od lewego gornego rogu.
    
    encoded_image = Image.new("RGB", image.size)
    pixels = encoded_image.load()
    
    for h in range(image.height):
        for w in range(image.width):
            
#            red = image.getpixel((w,h))[0]
#            binred=bin(red)
#            newbinred = binred[:-1] + next(bit)
#            newred = int(newbinred,2)
            
            newred = int(bin(image.getpixel((w,h))[0])[:-1] + next(bit),2)
            
#            green = image.getpixel((w,h))[1]
#            bingreen=bin(green)
#            newbingreen = bingreen[:-1] + next(bit)
#            newgreen = int(newbingreen,2)
            
            newgreen = int(bin(image.getpixel((w,h))[1])[:-1] + next(bit),2)
            
#            blue = image.getpixel((w,h))[2]
#            binblue=bin(blue)
#            newbinblue = binblue[:-1] + next(bit)
#            newblue = int(newbinblue,2)
            
            newblue = int(bin(image.getpixel((w,h))[2])[:-1] + next(bit),2)
            
            pixels[w,h] = (newred, newgreen, newblue)
    
    encoded_image.save("encoded_image.png")
    

#funkcja deszyfrujaca

def decoder(encoded_image_location):
    
    encoded_image = Image.open(encoded_image_location)
    
    #ekstrakcja najmniej znaczacego bitu z kanalow RGB kolejnych pikseli
    
    secret_letter = ""
    secret_message = ""
    for h in range(encoded_image.height):
        for w in range(encoded_image.width):
            for n in range(3):
                secret_bit = bin(encoded_image.getpixel((w,h))[n])[-1]
                secret_letter += secret_bit
                if len(secret_letter)==7 and secret_letter!="0000000":
                    ch = chr(int(secret_letter,2))
                    secret_message += ch
                    #print(ch)
                    secret_letter = ""
                if secret_letter == "0000000":
                    return print("Sekretna wiadomosc to: " + secret_message)

# funkcja podajaca dodatkowe informacje (do prezentacji na zajeciach).


def additional_info(image_location, encoded_image_location):

    image = Image.open(image_location)
    encoded_image=Image.open(encoded_image_location)    
    
    #maksymalna dlugosc wiadomosci mozliwa do zakodowania w danym obrazie
    
    total=image.height*image.width*3/7    
    print("W wybranym zdjeciu mozna zakodowac " + str(round(total)) + " znakow, czyli ok. " + str(round(total/1800)) + " stron.")
    
    #porownanie koloru losowego piksela przed i po kodowaniu

    before=0
    after=0
    while before==after:
        a = random.randint(0, 255)
        b = random.randint(0, 255)
        before = image.getpixel((a,b))[0:3]
        after = encoded_image.getpixel((a,b))
        col_b = '#%02x%02x%02x' % before
        col_a = '#%02x%02x%02x' % after
    
    vals = [['Oryginalne zdjecie', 'Zakodowane zdjecie'], [str(before), str(after)], ["",""]]
    cols = ["white","white",col_b,"white","white",col_a]
    
    trace = go.Table(
            header=dict(values=['<b>Obraz</b>', '<b>RGB</b>', '<b>Kolor</b>']),
            cells=dict(values=vals, fill = dict(color=cols), height = 30)
            )
    
    layout = dict(width=800, height=300, autosize=False,
                  title='Zmiana w kolorze losowego piksela po zakodowaniu')
    data = [trace]
    fig = dict(data=data, layout=layout)
    offline.plot(fig, image='png')


#wywolanie funkcji na przykladowym zdjeciu

image_location="example.png"
encoder(image_location)

encoded_image_location="encoded_image.png"
decoder(encoded_image_location)     

additional_info(image_location, encoded_image_location)  