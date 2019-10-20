# package load 시에 아래 순서로 import한다.
# 첫번째로 django로부터 모든것들 (파이썬이 있으면 파이썬이 첫번째)
# 두번쨰로 third-party의 것들
# 세번째로 나의 것들
from django.db import models
from core import models as core_models
from django_countries.fields import CountryField

# from users import models as user_models
# foreignkey나 manytomany에서 객체를 찾을 때 상하수직 순서대로 찾는다.
# 그래서 내가 line 50에서 객체 room을 찾을 때 room이 line 50보다 먼저 있는 것이 아니라
# line 60같은 곳에 있다면 찾을 수가 없다. 그래서 객체를 명시할 때
# foreignkey(room)이 아니라 foreignkey("room")으로 부르면 해결이 된다.


class AbstractItem(core_models.TimeStampedModel):

    """ Abstract Item """

    name = models.CharField(max_length=80)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class RoomType(AbstractItem):

    """ RoomType Model Definition """

    class Meta:
        verbose_name = "Room Type"
        ordering = ["name"]


class Amenity(AbstractItem):

    """ Amenity Model Definition """

    class Meta:
        verbose_name_plural = "Amenities"


class Facility(AbstractItem):

    """ Facility Model Definition """

    class Meta:
        verbose_name_plural = "Facilities"


class HouseRule(AbstractItem):

    """ HouseRule Model Definition """

    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    """ Photo Model Definition """

    caption = models.CharField(max_length=80)
    file = models.ImageField()
    room = models.ForeignKey("Room", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=140)
    price = models.IntegerField()

    guests = models.IntegerField()
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()

    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)

    # ForeignKey는 many-to-one relationship이다.
    # ondelete는 ForeignKey에만 해당한다.
    # CASCADE는 user를 삭제할 때 그 아래 딸린 room도 삭제된다는 것. - 폭포수처럼 -
    # room이 있는 유저는 삭제되지 않도록 protect할 수도 있다.
    # user가 삭제되면 모든 room들이 관리자에게 넘어가게 할 수도 있다.
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)

    # ManyToManyField는 many-to-many relationship이다.
    room_type = models.ForeignKey("RoomType", on_delete=models.SET_NULL, null=True)

    amenities = models.ManyToManyField("Amenity", blank=True)
    facilities = models.ManyToManyField("Facility", blank=True)
    house_rules = models.ManyToManyField("HouseRule", blank=True)

    # 사용자 이름으로 return해준다.
    def __str__(self):
        return self.name
