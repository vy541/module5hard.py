from time import sleep


class User:
    def __init__(self, nickname:str, password:int, age:int):
        self.nickname = nickname
        self.password = password
        self.age = age

    def __str__(self):
        return self.nickname


class Video:
    def __init__(self, title:str, duration:int, time_now:int=0, adult_mode:bool=False):
        self.title = title
        self.duration = duration
        self.time_now = time_now
        self.adult_mode = adult_mode


class UrTube:
     def __init__(self, users=[], videos=[], current_user: User = None):
        self.users = users
        self.videos = videos
        self.current_user = current_user

     def log_in(self, nickname: str, password: str):
         user = self.get_user(nickname)
         if user:
             if hash(password) == user.password:
                 self.current_user = user

     def register(self, nickname: str, password: str, age: int):
         if not self.get_user(nickname):
             self.users.append(User(nickname, hash(password), age))
             self.log_in(nickname, password)
         else:
             print(f'Пользователь {nickname} уже существует')

     def log_out(self):
         self.current_user = None

     def add(self, *videos: Video):
         for video in videos:
             if not self.get_video(video.title):
                 self.videos.append(video)

     def get_videos(self, search: str):
         found = []
         search = search.lower()
         for title in map(getattr, self.videos, ['title'] * len(self.videos)):
             if search in title.lower():
                 found.append(title)
         return found

     def watch_video(self, title: str):
         video = self.get_video(title)
         if video:
             if self.current_user:
                 if video.adult_mode and self.current_user.age < 18:
                     print('Вам нет 18 лет, пожалуйста покиньте страницу')
                 else:
                     while video.time_now < video.duration:
                         sleep(1)
                         video.time_now += 1
                         print(video.time_now, end=' ', flush=True)
                     video.time_now = 0
                     print('Конец видео')
             else:
                 print('Войдите в аккаунт, чтобы смотреть видео')

     def get_video(self, title: str):
         for video in self.videos:
             if title == video.title:
                 return video
         return None

     def get_user(self, nickname: str):
         for user in self.users:
             if nickname == user.nickname:
                 return user
         return None

ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')

