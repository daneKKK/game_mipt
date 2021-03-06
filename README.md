## Hopeless Dungeon

## Оглавление
1. Идея игры и геймлей.
2. Общая архитектура проекта:
a. game_main.py,
b. game_objects.py,
c. game_vis.py,
d. game_input.py,
i. Папка levels,
f. Папка resources,
3. Ссылки на используемые источники.

## Введение

Игра создавалась как курсовой проект по введению в программирование для ЛФИ МФТИ студентами группы Б02-105: Алексеев Даниил, Ромашкин Никита, Хомяков Никита, Ким Тимур.

## Идея игры и геймплей

Игра создавалась под вдохновением от игрового жанра roguelike, где смерть - часть игрового процесса и большая часть геймплея генерируется рандомно. Это выразилось в наборе уровней, который может легко расширяться, и заточенности геймплея под частые смерти (так, здоровье у игрока не восстанавливается при победе над врагами).

Центром геймплея является проход игрока по уровням, наполненным двумя видами врагов: пауками (ближний бой) и скелетами (дальний бой). Игрок может уничтожать их мечом или луком, меняемыми по нажатию кнопки F.

## Архитектура проекта

Проект состоит из 4 исполняемых файлов:

# game_main.py

Главный файл проекта, в котором хранятся функции, связанные с общей логикой игры (местонахождение игрока на уровне, искуственный интеллект, обработка нажатий клавиш, создание различных меню и т.д.).

# game_objects.py

Файл, хранящий информацию о всех классах (за исключением одного) проекта и их методах.

# game_vis.py

Файл, выводящий всю игровую информацию на экран (за исключением меню, которые выводятся сторонней библиотекой функциями, описанными в game_main.py). Большую часть этого он делает с помощью класса Drawer (единственный, описанный вне game_objects.py).

# game_input.py

Файл, сохраняющий и загружающий игру в файлы формата .json и загружающий информацию об уровнях из папки levels.

# Библиотека уровней

В проект заложена возможность загружать свои уровни в папку levels в соответствии с уже существующими. Взяв случайный уровень из библотеки, игра создаёт этот уровень.

# Сохранения и загрузка

Пусть сохранения и загрузка не отвечают жанру roguelike, они были созданы. Геймплей, однако, это не меняет (за исключением каких-нибудь крайних случаев перфекционизма с прохождением всех уровней без урона) ввиду невосполнимости здоровья.

## Используемые сторонние работы

В проекте использовались библиотека pygame-menu (на ней сделаны все меню), набор спрайтов orb game art (https://opengameart.org/content/orb-game-art#).


