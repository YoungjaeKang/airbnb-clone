# package load 시에 아래 순서로 import한다.
# 첫번째로 django로부터 모든것들 (파이썬이 있으면 파이썬이 첫번째)
# 두번쨰로 third-party의 것들
# 세번째로 나의 것들
from django.db import models
from django.urls import reverse
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
    file = models.ImageField(upload_to="room_photos")
    room = models.ForeignKey("Room", related_name="photos", on_delete=models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    """ Room Model Definition """

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=80)  # city도 country처럼 미리 만들어진 셋을 가져올 수 있다?
    address = models.CharField(max_length=140)
    price = models.IntegerField()

    guests = models.IntegerField(help_text="How many people will be staying?")
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
    host = models.ForeignKey(
        "users.User", related_name="rooms", on_delete=models.CASCADE
    )

    # ManyToManyField는 many-to-many relationship이다.
    room_type = models.ForeignKey(
        "RoomType", related_name="rooms", on_delete=models.SET_NULL, null=True
    )

    amenities = models.ManyToManyField("Amenity", related_name="rooms", blank=True)
    facilities = models.ManyToManyField("Facility", related_name="rooms", blank=True)
    house_rules = models.ManyToManyField("HouseRule", related_name="rooms", blank=True)

    # 사용자 이름으로 return해준다.
    def __str__(self):
        return self.name

    # 어드민이나 유저가 저장할 때 결과를 가로채는 함수인데 save_model을 쓰면 admin에서 변화만 감지한다.
    # 이 변화를 감지해서 누가 바꿨는지 혹은 바꿀 때 메일을 보내는 기능 등을 사용할 수 있다 !!
    def save(self, *args, **kwargs):
        self.city = str.capitalize(self.city)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={"pk": self.pk})

    def total_rating(self):
        all_reviews = self.reviews.all()
        all_ratings = 0
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return all_ratings / len(all_reviews)
        return 0

    def first_photo(self):
        print(self.photos.all()[:1])
        # 쿼리셋(어레이)에서 뭔가를 꺼낼 때 one, two, three, four = array[] 로 뽑을 수 있다. 사진은 1장이지만 배열로 되어 있기 때문에 ,를 붙여준다.
        photo, = self.photos.all()[:1] 
        return photo.file.url
        