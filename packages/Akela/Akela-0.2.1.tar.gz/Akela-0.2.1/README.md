Akela
=====

Akela - программа, которая скачивает веб-страницы и сохраняет их в
формате Markdown.

Использование
-------------

`Akela url path`

Программа создаст папку ~/.akela/library для 
сохранения файлов.

Новости
-------

### Akela 0.2

+ Добавлена функция чтения ZIM-файлов
+ Добавлена поддержка URI

#### Описание URI:

Cтрока `akela-zim//wikipedia/A/URI` значит взять документ
/A/URI из zim-файла, указанного в опции wikipedia 
секции Zim конфигурационного файла ~/.akela/bm.ini. 

##### Пример:


`from akela.uri import URI`

`locate = URI("akela-zim://wikisource/A/Человеческое,_слишком_человеческое_(Ницше)")`

`locate.parse()`

`open("test", "w").write(locate.resource)`


### Akela 0.1

Первый выпуск
