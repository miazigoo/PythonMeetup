from django.db import models
from django.utils import timezone


class Client(models.Model):
    telegram_id = models.IntegerField(unique=True)
    nik_name = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="UserName"
    )

    def __str__(self):
        return f"{self.nik_name}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Topic(models.Model):
    title = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="topic"
    )
    time_event = models.TimeField(null=True,
                                  blank=True, )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"


class Speaker(models.Model):
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='speakers')
    name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        verbose_name="Name"
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Спикер"
        verbose_name_plural = "Спикеры"


class EventQuerySet(models.QuerySet):

    def get_or_none(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except Event.DoesNotExist:
            return None


class Event(models.Model):
    topic = models.ManyToManyField(Topic)
    speaker = models.ManyToManyField(
        Speaker,
    )
    date = models.DateField(default=timezone.now)
    title = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        verbose_name="Title"
    )
    text = models.TextField()

    objects = EventQuerySet.as_manager()

    def __str__(self):
        return f"{self.title}"

    def display_topics(self):
        text = ''
        # text.join([str(topic.title) for topic in self.topic.all()])
        # text.join([str(speaker.name) for speaker in self.speaker.all()])
        for topic in self.topic.all().order_by('time_event'):
            for speaker in self.speaker.all():
                time_event = topic.time_event.strftime("%H:%M")
                text = text + f'В *{time_event}* {topic.title} - {speaker.name}\n'
        return text

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"


class Flag(models.Model):
    speaker = models.ForeignKey(Speaker,
                                on_delete=models.CASCADE,
                                related_name='speakers_flag')
    flag = models.BooleanField(
        default=False,
        null=True,
        blank=False,
    )

    def __str__(self):
        return f"{self.speaker} | {self.flag}"

    class Meta:
        verbose_name = "Флаг"
        verbose_name_plural = "Флаги"


class Question(models.Model):
    nikname = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="UserName"
    )
    text = models.TextField()
    speaker = models.ForeignKey(Speaker,
                                on_delete=models.CASCADE,
                                related_name='speaker_questions')

    def __str__(self):
        return f"Вопрос спикеру: {self.speaker.name} | от {self.nikname}"

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class ApplicationSpeaker(models.Model):
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='speakers_application')
    name = models.CharField(
        max_length=256,
        null=True,
        blank=False,
        verbose_name="Name"
    )
    topic = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        verbose_name="topic"
    )

    def __str__(self):
        return f"Заявка в спикеры от: {self.name}"

    class Meta:
        verbose_name = "Заявка в спикеры"
        verbose_name_plural = "Заявки в спикеры"
