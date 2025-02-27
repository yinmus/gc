
# Зависимости

- [`Python`](https://python.org)
  - [`requests`](https://pypi.org/project/requests/)
  - [`argparse`](https://docs.python.org/3/library/argparse.html)
  - [`os`](https://docs.python.org/3/library/os.html)
  - [`re`](https://docs.python.org/3/library/re.html)
  - [`sys`](https://docs.python.org/3/library/sys.html)
  - [`subprocess`](https://docs.python.org/3/library/subprocess.html)
 

___

## Установка

`Клон репозитория:`
```bash
git clone https://github.com/yinmus/gc.git
```

`Переход в директорию:`

```bash
cd gc
```

`Дать права на выполнение инсталлера:`

```bash
chmod +x gc_installer.sh
```

`Запустить инсталлер:`

```bash
./gc_installer.sh
```
___

## Использование:

### начну с довольно важного, потому-что без отсутствия этого будет много 403 error

 1. Зайдите на эту страницу [`github`](https://github.com/settings/tokens)
 2. Войдите в аккаунт
 3. Сгенерируйте `токен`, скопируйте его
 4. Установите `gc`
 5. Выполните команду:

     ```bash
     gc -T "токен, который вы [сгенерировали](https://github.com/settings/tokens)"
     ```
     При желании можно убедиться, что все правильно
     ```bash
     gc -Tl
     ```

### теперь ко всему остальному

`help`. Который даст список команд и их описание:
```bash
gc -h
```
`c`/`URL`. Для клона репозиториев:

- `c`:
 
  ```bash
  gc -c OWNER/repo  
  ```
- `URL`:
 
  ```bash
  gc https://github.com/OWNER/repo
  ```
`sr`. Для поиска репозиториев:

- `-sr`. Для простого поиска:
- 
  ```bash
  gc -sr examplerepo
  ```
- `-sr -k`. В поиске будет показывать размер репозитория:
 
  ```bash
  gc -sr examplerepo -k
  ```
- `-sr -p`. Будет показывать по популярности в звездах:
  
  ```bash
  gc -sr examplerepo -p
  ```
- `-sr -k -p`. Тут и так ясно:
  
  ```bash
  gc -sr examplerepo -k -p
  ```

`sur`. Для поиска репозиториев пользователя, логика такая-же, как и в `-sr`, только вместо имя репозитория стоит username. `-k`, `-p` - Тоже работают

`su`. Для поиска пользователей. Расписывать тоже не буду, и так ясно:

```bash
gc -su username
```

`so`. Для поиска организаций. Принцип тот-же, как и в `su`:

```bash
gc -so microsoft 
```
___
фууух, наконец-то 

