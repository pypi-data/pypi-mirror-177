# AUTO-GENERATED FILE. Do not edit. Run chalkpy stubgen to generate.
# fmt: off
# isort: skip_file
from __future__ import annotations

from chalk.features import DataFrame as DataFrame
from chalk.features import Features as Features
from chalk.features import Tags as Tags
from chalk.features.feature_set import FeaturesMeta as FeaturesMeta
from chalk.streams._windows import Windowed as __stubgen_chalk_streams___windows_Windowed
from chalk.utils.duration import Duration as Duration
from datetime import date as __stubgen_datetime_date
from datetime import datetime as __stubgen_datetime_datetime
from tests.client.test_client_serialization import Color as __stubgen_tests_client_test__client__serialization_Color
from tests.client.test_expand_features import Ankle as __stubgen_tests_client_test__expand__features_Ankle
from tests.client.test_expand_features import Foot as __stubgen_tests_client_test__expand__features_Foot
from tests.features.test_chained_feature_time import Homeowner as __stubgen_tests_features_test__chained__feature__time_Homeowner
from tests.features.test_chained_has_one import ExampleFraudOrg as __stubgen_tests_features_test__chained__has__one_ExampleFraudOrg
from tests.features.test_chained_has_one import ExampleFraudUser as __stubgen_tests_features_test__chained__has__one_ExampleFraudUser
from tests.features.test_df import Foo as __stubgen_tests_features_test__df_Foo
from tests.features.test_df import Topping as __stubgen_tests_features_test__df_Topping
from tests.features.test_df import ToppingPrice as __stubgen_tests_features_test__df_ToppingPrice
from tests.features.test_features import SingleChildFS as __stubgen_tests_features_test__features_SingleChildFS
from tests.features.test_features import SingleParentFS as __stubgen_tests_features_test__features_SingleParentFS
from tests.features.test_iter import NoFunFeatures as __stubgen_tests_features_test__iter_NoFunFeatures
from tests.serialization.test_codec import Color as __stubgen_tests_serialization_test__codec_Color
from tests.serialization.test_codec import CustomClass as __stubgen_tests_serialization_test__codec_CustomClass
from tests.serialization.test_codec import MyDataclass as __stubgen_tests_serialization_test__codec_MyDataclass
from typing import Optional as Optional
from typing import Protocol as Protocol
from typing import Type as Type
from typing import Union as Union
from typing import overload as overload

class WowFSMetaclass(FeaturesMeta):
    @property
    def something(self) -> Type[str]: ...

    @property
    def something_else(self) -> Type[str]: ...

    @property
    def nocomment(self) -> Type[str]: ...

    @property
    def nope(self) -> Type[str]: ...

    @property
    def assigned(self) -> Type[str]: ...

    @property
    def bizarre(self) -> Type[str]: ...

    @property
    def goofy(self) -> Type[str]: ...

    @property
    def assigned_comment(self) -> Type[str]: ...

    @property
    def explicit(self) -> Type[str]: ...

    @property
    def assigned_comment_multiline(self) -> Type[str]: ...

    @property
    def time(self) -> Type[__stubgen_datetime_datetime]: ...

    @property
    def nope_nope(self) -> Type[__stubgen_datetime_datetime]: ...

class WowFS(Features, metaclass=WowFSMetaclass):
    def __init__(
        self,
        something: str = ...,
        something_else: str = ...,
        nocomment: str = ...,
        nope: str = ...,
        assigned: str = ...,
        bizarre: str = ...,
        goofy: str = ...,
        assigned_comment: str = ...,
        explicit: str = ...,
        assigned_comment_multiline: str = ...,
        time: __stubgen_datetime_datetime = ...,
        nope_nope: __stubgen_datetime_datetime = ...,
    ):
        self.something: str
        self.something_else: str
        self.nocomment: str
        self.nope: str
        self.assigned: str
        self.bizarre: str
        self.goofy: str
        self.assigned_comment: str
        self.explicit: str
        self.assigned_comment_multiline: str
        self.time: __stubgen_datetime_datetime
        self.nope_nope: __stubgen_datetime_datetime

class WowFSProtocol(Protocol):
    something: str
    something_else: str
    nocomment: str
    nope: str
    assigned: str
    bizarre: str
    goofy: str
    assigned_comment: str
    explicit: str
    assigned_comment_multiline: str
    time: __stubgen_datetime_datetime
    nope_nope: __stubgen_datetime_datetime

class TacoMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def user_id(self) -> Type[str]: ...

    @property
    def price(self) -> Type[int]: ...

    @property
    def maybe_price(self) -> Type[Union[int, None]]: ...

    @property
    def hat(self) -> Type[str]: ...

    @property
    def topping_id(self) -> Type[str]: ...

    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

    @property
    def nicknames(self) -> Type[DataFrame]: ...

    @property
    def topping(self) -> Type[__stubgen_tests_features_test__df_Topping]: ...

    @property
    def foo(self) -> Type[__stubgen_tests_features_test__df_Foo]: ...

    @property
    def foos(self) -> Type[list[__stubgen_tests_features_test__df_Foo]]: ...

class Taco(Features, metaclass=TacoMetaclass):
    def __init__(
        self,
        id: str = ...,
        user_id: str = ...,
        price: int = ...,
        maybe_price: Union[int, None] = ...,
        hat: str = ...,
        topping_id: str = ...,
        ts: __stubgen_datetime_datetime = ...,
        nicknames: DataFrame = ...,
        topping: __stubgen_tests_features_test__df_Topping = ...,
        foo: __stubgen_tests_features_test__df_Foo = ...,
        foos: list[__stubgen_tests_features_test__df_Foo] = ...,
    ):
        self.id: str
        self.user_id: str
        self.price: int
        self.maybe_price: Union[int, None]
        self.hat: str
        self.topping_id: str
        self.ts: __stubgen_datetime_datetime
        self.nicknames: DataFrame
        self.topping: __stubgen_tests_features_test__df_Topping
        self.foo: __stubgen_tests_features_test__df_Foo
        self.foos: list[__stubgen_tests_features_test__df_Foo]

class TacoProtocol(Protocol):
    id: str
    user_id: str
    price: int
    maybe_price: Union[int, None]
    hat: str
    topping_id: str
    ts: __stubgen_datetime_datetime
    nicknames: DataFrame
    topping: __stubgen_tests_features_test__df_Topping
    foo: __stubgen_tests_features_test__df_Foo
    foos: list[__stubgen_tests_features_test__df_Foo]

class HelloMetaclass(FeaturesMeta):
    @property
    def a(self) -> Type[str]: ...

    @property
    def b(self) -> Type[int]: ...

    @property
    def c(self) -> Type[__stubgen_datetime_datetime]: ...

    @property
    def d(self) -> Type[__stubgen_tests_serialization_test__codec_Color]: ...

    @property
    def e(self) -> Type[__stubgen_datetime_date]: ...

    @property
    def f(self) -> Type[__stubgen_tests_serialization_test__codec_MyDataclass]: ...

    @property
    def y(self) -> Type[set[int]]: ...

    @property
    def z(self) -> Type[list[str]]: ...

    @property
    def fancy(self) -> Type[__stubgen_tests_serialization_test__codec_CustomClass]: ...

class Hello(Features, metaclass=HelloMetaclass):
    def __init__(
        self,
        a: str = ...,
        b: int = ...,
        c: __stubgen_datetime_datetime = ...,
        d: __stubgen_tests_serialization_test__codec_Color = ...,
        e: __stubgen_datetime_date = ...,
        f: __stubgen_tests_serialization_test__codec_MyDataclass = ...,
        y: set[int] = ...,
        z: list[str] = ...,
        fancy: __stubgen_tests_serialization_test__codec_CustomClass = ...,
    ):
        self.a: str
        self.b: int
        self.c: __stubgen_datetime_datetime
        self.d: __stubgen_tests_serialization_test__codec_Color
        self.e: __stubgen_datetime_date
        self.f: __stubgen_tests_serialization_test__codec_MyDataclass
        self.y: set[int]
        self.z: list[str]
        self.fancy: __stubgen_tests_serialization_test__codec_CustomClass

class HelloProtocol(Protocol):
    a: str
    b: int
    c: __stubgen_datetime_datetime
    d: __stubgen_tests_serialization_test__codec_Color
    e: __stubgen_datetime_date
    f: __stubgen_tests_serialization_test__codec_MyDataclass
    y: set[int]
    z: list[str]
    fancy: __stubgen_tests_serialization_test__codec_CustomClass

class MappingFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def u_from(self) -> Type[str]: ...

    @property
    def u_to(self) -> Type[str]: ...

    @property
    def column_a(self) -> Type[str]: ...

    @property
    def swap_b(self) -> Type[str]: ...

    @property
    def swap_c(self) -> Type[str]: ...

class MappingFeatures(Features, metaclass=MappingFeaturesMetaclass):
    def __init__(
        self,
        id: int = ...,
        u_from: str = ...,
        u_to: str = ...,
        column_a: str = ...,
        swap_b: str = ...,
        swap_c: str = ...,
    ):
        self.id: int
        self.u_from: str
        self.u_to: str
        self.column_a: str
        self.swap_b: str
        self.swap_c: str

class MappingFeaturesProtocol(Protocol):
    id: int
    u_from: str
    u_to: str
    column_a: str
    swap_b: str
    swap_c: str

class CommentBaseOwnerMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def empty(self) -> Type[str]: ...

    @property
    def email(self) -> Type[str]: ...

    @property
    def email_commas(self) -> Type[str]: ...

    @property
    def email_single(self) -> Type[str]: ...

    @property
    def email_all_kinds(self) -> Type[str]: ...

class CommentBaseOwner(Features, metaclass=CommentBaseOwnerMetaclass):
    def __init__(
        self,
        id: str = ...,
        empty: str = ...,
        email: str = ...,
        email_commas: str = ...,
        email_single: str = ...,
        email_all_kinds: str = ...,
    ):
        self.id: str
        self.empty: str
        self.email: str
        self.email_commas: str
        self.email_single: str
        self.email_all_kinds: str

class CommentBaseOwnerProtocol(Protocol):
    id: str
    empty: str
    email: str
    email_commas: str
    email_single: str
    email_all_kinds: str

class ToppingMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def value(self) -> Type[int]: ...

    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

    @property
    def nicknames(self) -> Type[DataFrame]: ...

    @property
    def price(self) -> Type[__stubgen_tests_features_test__df_ToppingPrice]: ...

class Topping(Features, metaclass=ToppingMetaclass):
    def __init__(
        self,
        id: str = ...,
        value: int = ...,
        ts: __stubgen_datetime_datetime = ...,
        nicknames: DataFrame = ...,
        price: __stubgen_tests_features_test__df_ToppingPrice = ...,
    ):
        self.id: str
        self.value: int
        self.ts: __stubgen_datetime_datetime
        self.nicknames: DataFrame
        self.price: __stubgen_tests_features_test__df_ToppingPrice

class ToppingProtocol(Protocol):
    id: str
    value: int
    ts: __stubgen_datetime_datetime
    nicknames: DataFrame
    price: __stubgen_tests_features_test__df_ToppingPrice

class PersonMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def name(self) -> Type[str]: ...

    @property
    def best_foot_id(self) -> Type[int]: ...

    @property
    def best_foot(self) -> Type[__stubgen_tests_client_test__expand__features_Foot]: ...

    @property
    def feet(self) -> Type[DataFrame]: ...

class Person(Features, metaclass=PersonMetaclass):
    def __init__(
        self,
        id: int = ...,
        name: str = ...,
        best_foot_id: int = ...,
        best_foot: __stubgen_tests_client_test__expand__features_Foot = ...,
        feet: DataFrame = ...,
    ):
        self.id: int
        self.name: str
        self.best_foot_id: int
        self.best_foot: __stubgen_tests_client_test__expand__features_Foot
        self.feet: DataFrame

class PersonProtocol(Protocol):
    id: int
    name: str
    best_foot_id: int
    best_foot: __stubgen_tests_client_test__expand__features_Foot
    feet: DataFrame

class HomeFeaturesChainedFeatureTimeMetaclass(FeaturesMeta):
    @property
    def home_id(self) -> Type[str]: ...

    @property
    def address(self) -> Type[str]: ...

    @property
    def price(self) -> Type[int]: ...

    @property
    def sq_ft(self) -> Type[int]: ...

    @property
    def homeowner(self) -> Type[__stubgen_tests_features_test__chained__feature__time_Homeowner]: ...

class HomeFeaturesChainedFeatureTime(Features, metaclass=HomeFeaturesChainedFeatureTimeMetaclass):
    def __init__(
        self,
        home_id: str = ...,
        address: str = ...,
        price: int = ...,
        sq_ft: int = ...,
        homeowner: __stubgen_tests_features_test__chained__feature__time_Homeowner = ...,
    ):
        self.home_id: str
        self.address: str
        self.price: int
        self.sq_ft: int
        self.homeowner: __stubgen_tests_features_test__chained__feature__time_Homeowner

class HomeFeaturesChainedFeatureTimeProtocol(Protocol):
    home_id: str
    address: str
    price: int
    sq_ft: int
    homeowner: __stubgen_tests_features_test__chained__feature__time_Homeowner

class FootMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def is_flat(self) -> Type[bool]: ...

    @property
    def person_id(self) -> Type[int]: ...

    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

    @property
    def ankle(self) -> Type[__stubgen_tests_client_test__expand__features_Ankle]: ...

class Foot(Features, metaclass=FootMetaclass):
    def __init__(
        self,
        id: int = ...,
        is_flat: bool = ...,
        person_id: int = ...,
        ts: __stubgen_datetime_datetime = ...,
        ankle: __stubgen_tests_client_test__expand__features_Ankle = ...,
    ):
        self.id: int
        self.is_flat: bool
        self.person_id: int
        self.ts: __stubgen_datetime_datetime
        self.ankle: __stubgen_tests_client_test__expand__features_Ankle

class FootProtocol(Protocol):
    id: int
    is_flat: bool
    person_id: int
    ts: __stubgen_datetime_datetime
    ankle: __stubgen_tests_client_test__expand__features_Ankle

class TransactionMetaclass(FeaturesMeta):
    @property
    def user_id(self) -> Type[str]: ...

    @property
    def amount(self) -> Type[int]: ...

    @property
    def source_account_id(self) -> Type[int]: ...

    @property
    def dest_account_id(self) -> Type[int]: ...

class Transaction(Features, metaclass=TransactionMetaclass):
    def __init__(
        self,
        user_id: str = ...,
        amount: int = ...,
        source_account_id: int = ...,
        dest_account_id: int = ...,
    ):
        self.user_id: str
        self.amount: int
        self.source_account_id: int
        self.dest_account_id: int

class TransactionProtocol(Protocol):
    user_id: str
    amount: int
    source_account_id: int
    dest_account_id: int

class ToppingPriceMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def topping_id(self) -> Type[str]: ...

    @property
    def wow(self) -> Type[str]: ...

    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

class ToppingPrice(Features, metaclass=ToppingPriceMetaclass):
    def __init__(
        self,
        id: str = ...,
        topping_id: str = ...,
        wow: str = ...,
        ts: __stubgen_datetime_datetime = ...,
    ):
        self.id: str
        self.topping_id: str
        self.wow: str
        self.ts: __stubgen_datetime_datetime

class ToppingPriceProtocol(Protocol):
    id: str
    topping_id: str
    wow: str
    ts: __stubgen_datetime_datetime

class TagFeaturesMetaclass(FeaturesMeta):
    @property
    def empty(self) -> Type[str]: ...

    @property
    def one(self) -> Type[str]: ...

    @property
    def many(self) -> Type[str]: ...

    @property
    def ft(self) -> Type[__stubgen_datetime_datetime]: ...

class TagFeatures(Features, metaclass=TagFeaturesMetaclass):
    def __init__(
        self,
        empty: str = ...,
        one: str = ...,
        many: str = ...,
        ft: __stubgen_datetime_datetime = ...,
    ):
        self.empty: str
        self.one: str
        self.many: str
        self.ft: __stubgen_datetime_datetime

class TagFeaturesProtocol(Protocol):
    empty: str
    one: str
    many: str
    ft: __stubgen_datetime_datetime

class ParentFSMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def children(self) -> Type[DataFrame]: ...

    @property
    def single_child(self) -> Type[__stubgen_tests_features_test__features_SingleChildFS]: ...

    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

class ParentFS(Features, metaclass=ParentFSMetaclass):
    def __init__(
        self,
        id: str = ...,
        children: DataFrame = ...,
        single_child: __stubgen_tests_features_test__features_SingleChildFS = ...,
        ts: __stubgen_datetime_datetime = ...,
    ):
        self.id: str
        self.children: DataFrame
        self.single_child: __stubgen_tests_features_test__features_SingleChildFS
        self.ts: __stubgen_datetime_datetime

class ParentFSProtocol(Protocol):
    id: str
    children: DataFrame
    single_child: __stubgen_tests_features_test__features_SingleChildFS
    ts: __stubgen_datetime_datetime

class OwnerFeaturesMetaclass(FeaturesMeta):
    @property
    def plain(self) -> Type[str]: ...

    @property
    def cached(self) -> Type[str]: ...

    @property
    def andy(self) -> Type[str]: ...

    @property
    def ft(self) -> Type[__stubgen_datetime_datetime]: ...

class OwnerFeatures(Features, metaclass=OwnerFeaturesMetaclass):
    def __init__(
        self,
        plain: str = ...,
        cached: str = ...,
        andy: str = ...,
        ft: __stubgen_datetime_datetime = ...,
    ):
        self.plain: str
        self.cached: str
        self.andy: str
        self.ft: __stubgen_datetime_datetime

class OwnerFeaturesProtocol(Protocol):
    plain: str
    cached: str
    andy: str
    ft: __stubgen_datetime_datetime

class MypyUserFeaturesMetaclass(FeaturesMeta):
    @property
    def uid(self) -> Type[str]: ...

    @property
    def name(self) -> Type[str]: ...

    @property
    def bday(self) -> Type[str]: ...

    @property
    def age(self) -> Type[int]: ...

class MypyUserFeatures(Features, metaclass=MypyUserFeaturesMetaclass):
    def __init__(
        self,
        uid: str = ...,
        name: str = ...,
        bday: str = ...,
        age: int = ...,
    ):
        self.uid: str
        self.name: str
        self.bday: str
        self.age: int

class MypyUserFeaturesProtocol(Protocol):
    uid: str
    name: str
    bday: str
    age: int

class HomeFeaturesMetaclass(FeaturesMeta):
    @property
    def home_id(self) -> Type[str]: ...

    @property
    def address(self) -> Type[str]: ...

    @property
    def price(self) -> Type[int]: ...

    @property
    def sq_ft(self) -> Type[int]: ...

class HomeFeatures(Features, metaclass=HomeFeaturesMetaclass):
    def __init__(
        self,
        home_id: str = ...,
        address: str = ...,
        price: int = ...,
        sq_ft: int = ...,
    ):
        self.home_id: str
        self.address: str
        self.price: int
        self.sq_ft: int

class HomeFeaturesProtocol(Protocol):
    home_id: str
    address: str
    price: int
    sq_ft: int

class FunFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def nope(self) -> Type[str]: ...

    @property
    def single_parent(self) -> Type[__stubgen_tests_features_test__iter_NoFunFeatures]: ...

    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

class FunFeatures(Features, metaclass=FunFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
        nope: str = ...,
        single_parent: __stubgen_tests_features_test__iter_NoFunFeatures = ...,
        ts: __stubgen_datetime_datetime = ...,
    ):
        self.id: str
        self.nope: str
        self.single_parent: __stubgen_tests_features_test__iter_NoFunFeatures
        self.ts: __stubgen_datetime_datetime

class FunFeaturesProtocol(Protocol):
    id: str
    nope: str
    single_parent: __stubgen_tests_features_test__iter_NoFunFeatures
    ts: __stubgen_datetime_datetime

class UserProfileMetaclass(FeaturesMeta):
    @property
    def user_id(self) -> Type[str]: ...

    @property
    def profile_id(self) -> Type[str]: ...

    @property
    def address(self) -> Type[int]: ...

class UserProfile(Features, metaclass=UserProfileMetaclass):
    def __init__(
        self,
        user_id: str = ...,
        profile_id: str = ...,
        address: int = ...,
    ):
        self.user_id: str
        self.profile_id: str
        self.address: int

class UserProfileProtocol(Protocol):
    user_id: str
    profile_id: str
    address: int

class UserMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def fav_color(self) -> Type[__stubgen_tests_client_test__client__serialization_Color]: ...

    @property
    def birthday(self) -> Type[__stubgen_datetime_date]: ...

class User(Features, metaclass=UserMetaclass):
    def __init__(
        self,
        id: int = ...,
        fav_color: __stubgen_tests_client_test__client__serialization_Color = ...,
        birthday: __stubgen_datetime_date = ...,
    ):
        self.id: int
        self.fav_color: __stubgen_tests_client_test__client__serialization_Color
        self.birthday: __stubgen_datetime_date

class UserProtocol(Protocol):
    id: int
    fav_color: __stubgen_tests_client_test__client__serialization_Color
    birthday: __stubgen_datetime_date

class SQLFriendsWithRowMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def u_from(self) -> Type[str]: ...

    @property
    def u_to(self) -> Type[str]: ...

class SQLFriendsWithRow(Features, metaclass=SQLFriendsWithRowMetaclass):
    def __init__(
        self,
        id: int = ...,
        u_from: str = ...,
        u_to: str = ...,
    ):
        self.id: int
        self.u_from: str
        self.u_to: str

class SQLFriendsWithRowProtocol(Protocol):
    id: int
    u_from: str
    u_to: str

class OtherPrimaryKeyFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def nah_really_this_is_id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class OtherPrimaryKeyFeatures(Features, metaclass=OtherPrimaryKeyFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
        nah_really_this_is_id: str = ...,
        other: str = ...,
    ):
        self.id: str
        self.nah_really_this_is_id: str
        self.other: str

class OtherPrimaryKeyFeaturesProtocol(Protocol):
    id: str
    nah_really_this_is_id: str
    other: str

class MaxStalenessFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def name(self) -> Type[str]: ...

    @property
    def woohoo(self) -> Type[str]: ...

class MaxStalenessFeatures(Features, metaclass=MaxStalenessFeaturesMetaclass):
    def __init__(
        self,
        id: int = ...,
        name: str = ...,
        woohoo: str = ...,
    ):
        self.id: int
        self.name: str
        self.woohoo: str

class MaxStalenessFeaturesProtocol(Protocol):
    id: int
    name: str
    woohoo: str

class HomeownerMetaclass(FeaturesMeta):
    @property
    def fullname(self) -> Type[str]: ...

    @property
    def home_id(self) -> Type[str]: ...

    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

class Homeowner(Features, metaclass=HomeownerMetaclass):
    def __init__(
        self,
        fullname: str = ...,
        home_id: str = ...,
        ts: __stubgen_datetime_datetime = ...,
    ):
        self.fullname: str
        self.home_id: str
        self.ts: __stubgen_datetime_datetime

class HomeownerProtocol(Protocol):
    fullname: str
    home_id: str
    ts: __stubgen_datetime_datetime

class ETLFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def name(self) -> Type[str]: ...

    @property
    def woohoo(self) -> Type[str]: ...

class ETLFeatures(Features, metaclass=ETLFeaturesMetaclass):
    def __init__(
        self,
        id: int = ...,
        name: str = ...,
        woohoo: str = ...,
    ):
        self.id: int
        self.name: str
        self.woohoo: str

class ETLFeaturesProtocol(Protocol):
    id: int
    name: str
    woohoo: str

class ChildFSMetaclass(FeaturesMeta):
    @property
    def parent_id(self) -> Type[str]: ...

    @property
    def parents(self) -> Type[DataFrame]: ...

    @property
    def single_parent(self) -> Type[__stubgen_tests_features_test__features_SingleParentFS]: ...

class ChildFS(Features, metaclass=ChildFSMetaclass):
    def __init__(
        self,
        parent_id: str = ...,
        parents: DataFrame = ...,
        single_parent: __stubgen_tests_features_test__features_SingleParentFS = ...,
    ):
        self.parent_id: str
        self.parents: DataFrame
        self.single_parent: __stubgen_tests_features_test__features_SingleParentFS

class ChildFSProtocol(Protocol):
    parent_id: str
    parents: DataFrame
    single_parent: __stubgen_tests_features_test__features_SingleParentFS

class UnassignedIdFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class UnassignedIdFeatures(Features, metaclass=UnassignedIdFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
        other: str = ...,
    ):
        self.id: str
        self.other: str

class UnassignedIdFeaturesProtocol(Protocol):
    id: str
    other: str

class UnassignedDecoratedIdFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class UnassignedDecoratedIdFeatures(Features, metaclass=UnassignedDecoratedIdFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
        other: str = ...,
    ):
        self.id: str
        self.other: str

class UnassignedDecoratedIdFeaturesProtocol(Protocol):
    id: str
    other: str

class TheArtistFormerlyKnownAsPrinceMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def favorite_color(self) -> Type[str]: ...

class TheArtistFormerlyKnownAsPrince(Features, metaclass=TheArtistFormerlyKnownAsPrinceMetaclass):
    def __init__(
        self,
        id: str = ...,
        favorite_color: str = ...,
    ):
        self.id: str
        self.favorite_color: str

class TheArtistFormerlyKnownAsPrinceProtocol(Protocol):
    id: str
    favorite_color: str

class StreamFeaturesWindowMetaclass(FeaturesMeta):
    @property
    def scalar_feature(self) -> Type[__stubgen_chalk_streams___windows_Windowed]: ...

    @property
    def uid(self) -> Type[str]: ...

class StreamFeaturesWindow(Features, metaclass=StreamFeaturesWindowMetaclass):
    def __init__(
        self,
        scalar_feature: __stubgen_chalk_streams___windows_Windowed = ...,
        uid: str = ...,
    ):
        self.scalar_feature: __stubgen_chalk_streams___windows_Windowed
        self.uid: str

class StreamFeaturesWindowProtocol(Protocol):
    scalar_feature: __stubgen_chalk_streams___windows_Windowed
    uid: str

class SingleParentFSMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def children(self) -> Type[DataFrame]: ...

class SingleParentFS(Features, metaclass=SingleParentFSMetaclass):
    def __init__(
        self,
        id: str = ...,
        children: DataFrame = ...,
    ):
        self.id: str
        self.children: DataFrame

class SingleParentFSProtocol(Protocol):
    id: str
    children: DataFrame

class SingleChildFSMetaclass(FeaturesMeta):
    @property
    def parent_id(self) -> Type[str]: ...

    @property
    def parent(self) -> Type[DataFrame]: ...

class SingleChildFS(Features, metaclass=SingleChildFSMetaclass):
    def __init__(
        self,
        parent_id: str = ...,
        parent: DataFrame = ...,
    ):
        self.parent_id: str
        self.parent: DataFrame

class SingleChildFSProtocol(Protocol):
    parent_id: str
    parent: DataFrame

class SQLUserFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def name(self) -> Type[str]: ...

class SQLUserFeatures(Features, metaclass=SQLUserFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
        name: str = ...,
    ):
        self.id: str
        self.name: str

class SQLUserFeaturesProtocol(Protocol):
    id: str
    name: str

class NotIdIsIdFeaturesMetaclass(FeaturesMeta):
    @property
    def not_id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class NotIdIsIdFeatures(Features, metaclass=NotIdIsIdFeaturesMetaclass):
    def __init__(
        self,
        not_id: str = ...,
        other: str = ...,
    ):
        self.not_id: str
        self.other: str

class NotIdIsIdFeaturesProtocol(Protocol):
    not_id: str
    other: str

class IdIsNotIdFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class IdIsNotIdFeatures(Features, metaclass=IdIsNotIdFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
        other: str = ...,
    ):
        self.id: str
        self.other: str

class IdIsNotIdFeaturesProtocol(Protocol):
    id: str
    other: str

class ExplicitIdFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class ExplicitIdFeatures(Features, metaclass=ExplicitIdFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
        other: str = ...,
    ):
        self.id: str
        self.other: str

class ExplicitIdFeaturesProtocol(Protocol):
    id: str
    other: str

class ExampleFraudUserMetaclass(FeaturesMeta):
    @property
    def uid(self) -> Type[str]: ...

    @property
    def org(self) -> Type[__stubgen_tests_features_test__chained__has__one_ExampleFraudOrg]: ...

class ExampleFraudUser(Features, metaclass=ExampleFraudUserMetaclass):
    def __init__(
        self,
        uid: str = ...,
        org: __stubgen_tests_features_test__chained__has__one_ExampleFraudOrg = ...,
    ):
        self.uid: str
        self.org: __stubgen_tests_features_test__chained__has__one_ExampleFraudOrg

class ExampleFraudUserProtocol(Protocol):
    uid: str
    org: __stubgen_tests_features_test__chained__has__one_ExampleFraudOrg

class ExampleFraudProfileMetaclass(FeaturesMeta):
    @property
    def uid(self) -> Type[str]: ...

    @property
    def user(self) -> Type[__stubgen_tests_features_test__chained__has__one_ExampleFraudUser]: ...

class ExampleFraudProfile(Features, metaclass=ExampleFraudProfileMetaclass):
    def __init__(
        self,
        uid: str = ...,
        user: __stubgen_tests_features_test__chained__has__one_ExampleFraudUser = ...,
    ):
        self.uid: str
        self.user: __stubgen_tests_features_test__chained__has__one_ExampleFraudUser

class ExampleFraudProfileProtocol(Protocol):
    uid: str
    user: __stubgen_tests_features_test__chained__has__one_ExampleFraudUser

class ExampleFraudOrgMetaclass(FeaturesMeta):
    @property
    def uid(self) -> Type[str]: ...

    @property
    def org_name(self) -> Type[str]: ...

class ExampleFraudOrg(Features, metaclass=ExampleFraudOrgMetaclass):
    def __init__(
        self,
        uid: str = ...,
        org_name: str = ...,
    ):
        self.uid: str
        self.org_name: str

class ExampleFraudOrgProtocol(Protocol):
    uid: str
    org_name: str

class CustomNameClassMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class CustomNameClass(Features, metaclass=CustomNameClassMetaclass):
    def __init__(
        self,
        id: str = ...,
        other: str = ...,
    ):
        self.id: str
        self.other: str

class CustomNameClassProtocol(Protocol):
    id: str
    other: str

class BogusIdFeature3Metaclass(FeaturesMeta):
    @property
    def id(self) -> Type[__stubgen_datetime_datetime]: ...

    @property
    def other(self) -> Type[str]: ...

class BogusIdFeature3(Features, metaclass=BogusIdFeature3Metaclass):
    def __init__(
        self,
        id: __stubgen_datetime_datetime = ...,
        other: str = ...,
    ):
        self.id: __stubgen_datetime_datetime
        self.other: str

class BogusIdFeature3Protocol(Protocol):
    id: __stubgen_datetime_datetime
    other: str

class BogusIdFeature2Metaclass(FeaturesMeta):
    @property
    def id(self) -> Type[DataFrame]: ...

    @property
    def other(self) -> Type[str]: ...

class BogusIdFeature2(Features, metaclass=BogusIdFeature2Metaclass):
    def __init__(
        self,
        id: DataFrame = ...,
        other: str = ...,
    ):
        self.id: DataFrame
        self.other: str

class BogusIdFeature2Protocol(Protocol):
    id: DataFrame
    other: str

class BogusIdFeature1Metaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def other(self) -> Type[str]: ...

class BogusIdFeature1(Features, metaclass=BogusIdFeature1Metaclass):
    def __init__(
        self,
        id: str = ...,
        other: str = ...,
    ):
        self.id: str
        self.other: str

class BogusIdFeature1Protocol(Protocol):
    id: str
    other: str

class AnkleMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[int]: ...

    @property
    def foot_id(self) -> Type[int]: ...

class Ankle(Features, metaclass=AnkleMetaclass):
    def __init__(
        self,
        id: int = ...,
        foot_id: int = ...,
    ):
        self.id: int
        self.foot_id: int

class AnkleProtocol(Protocol):
    id: int
    foot_id: int

class AcctMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

    @property
    def balance(self) -> Type[float]: ...

class Acct(Features, metaclass=AcctMetaclass):
    def __init__(
        self,
        id: str = ...,
        balance: float = ...,
    ):
        self.id: str
        self.balance: float

class AcctProtocol(Protocol):
    id: str
    balance: float

class AccountMetaclass(FeaturesMeta):
    @property
    def account_id(self) -> Type[str]: ...

    @property
    def balance(self) -> Type[int]: ...

class Account(Features, metaclass=AccountMetaclass):
    def __init__(
        self,
        account_id: str = ...,
        balance: int = ...,
    ):
        self.account_id: str
        self.balance: int

class AccountProtocol(Protocol):
    account_id: str
    balance: int

class UserFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

class UserFeatures(Features, metaclass=UserFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
    ):
        self.id: str

class UserFeaturesProtocol(Protocol):
    id: str

class StreamFeaturesMetaclass(FeaturesMeta):
    @property
    def scalar_feature(self) -> Type[str]: ...

class StreamFeatures(Features, metaclass=StreamFeaturesMetaclass):
    def __init__(
        self,
        scalar_feature: str = ...,
    ):
        self.scalar_feature: str

class StreamFeaturesProtocol(Protocol):
    scalar_feature: str

class NoFunFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

class NoFunFeatures(Features, metaclass=NoFunFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
    ):
        self.id: str

class NoFunFeaturesProtocol(Protocol):
    id: str

class NicknameMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

class Nickname(Features, metaclass=NicknameMetaclass):
    def __init__(
        self,
        id: str = ...,
    ):
        self.id: str

class NicknameProtocol(Protocol):
    id: str

class LibraryFeaturesMetaclass(FeaturesMeta):
    @property
    def id(self) -> Type[str]: ...

class LibraryFeatures(Features, metaclass=LibraryFeaturesMetaclass):
    def __init__(
        self,
        id: str = ...,
    ):
        self.id: str

class LibraryFeaturesProtocol(Protocol):
    id: str

class FeaturesClassWithNamedTsMetaclass(FeaturesMeta):
    @property
    def ts(self) -> Type[__stubgen_datetime_datetime]: ...

class FeaturesClassWithNamedTs(Features, metaclass=FeaturesClassWithNamedTsMetaclass):
    def __init__(
        self,
        ts: __stubgen_datetime_datetime = ...,
    ):
        self.ts: __stubgen_datetime_datetime

class FeaturesClassWithNamedTsProtocol(Protocol):
    ts: __stubgen_datetime_datetime

class FeaturesClassWithCustomTsNameMetaclass(FeaturesMeta):
    @property
    def ts_custom_name(self) -> Type[__stubgen_datetime_datetime]: ...

class FeaturesClassWithCustomTsName(Features, metaclass=FeaturesClassWithCustomTsNameMetaclass):
    def __init__(
        self,
        ts_custom_name: __stubgen_datetime_datetime = ...,
    ):
        self.ts_custom_name: __stubgen_datetime_datetime

class FeaturesClassWithCustomTsNameProtocol(Protocol):
    ts_custom_name: __stubgen_datetime_datetime

class FeaturesClassWithoutTimestampMetaclass(FeaturesMeta):
    ...

class FeaturesClassWithoutTimestamp(Features, metaclass=FeaturesClassWithoutTimestampMetaclass):
    def __init__(
        self,
    ):
        ...

class FeaturesClassWithoutTimestampProtocol(Protocol):
    ...

@overload
def features(item: Type[WowFSProtocol]) -> Type[WowFS]: ...

@overload
def features(item: Type[TacoProtocol]) -> Type[Taco]: ...

@overload
def features(item: Type[HelloProtocol]) -> Type[Hello]: ...

@overload
def features(item: Type[MappingFeaturesProtocol]) -> Type[MappingFeatures]: ...

@overload
def features(item: Type[CommentBaseOwnerProtocol]) -> Type[CommentBaseOwner]: ...

@overload
def features(item: Type[ToppingProtocol]) -> Type[Topping]: ...

@overload
def features(item: Type[PersonProtocol]) -> Type[Person]: ...

@overload
def features(item: Type[HomeFeaturesChainedFeatureTimeProtocol]) -> Type[HomeFeaturesChainedFeatureTime]: ...

@overload
def features(item: Type[FootProtocol]) -> Type[Foot]: ...

@overload
def features(item: Type[TransactionProtocol]) -> Type[Transaction]: ...

@overload
def features(item: Type[ToppingPriceProtocol]) -> Type[ToppingPrice]: ...

@overload
def features(item: Type[TagFeaturesProtocol]) -> Type[TagFeatures]: ...

@overload
def features(item: Type[ParentFSProtocol]) -> Type[ParentFS]: ...

@overload
def features(item: Type[OwnerFeaturesProtocol]) -> Type[OwnerFeatures]: ...

@overload
def features(item: Type[MypyUserFeaturesProtocol]) -> Type[MypyUserFeatures]: ...

@overload
def features(item: Type[HomeFeaturesProtocol]) -> Type[HomeFeatures]: ...

@overload
def features(item: Type[FunFeaturesProtocol]) -> Type[FunFeatures]: ...

@overload
def features(item: Type[UserProfileProtocol]) -> Type[UserProfile]: ...

@overload
def features(item: Type[UserProtocol]) -> Type[User]: ...

@overload
def features(item: Type[SQLFriendsWithRowProtocol]) -> Type[SQLFriendsWithRow]: ...

@overload
def features(item: Type[OtherPrimaryKeyFeaturesProtocol]) -> Type[OtherPrimaryKeyFeatures]: ...

@overload
def features(item: Type[MaxStalenessFeaturesProtocol]) -> Type[MaxStalenessFeatures]: ...

@overload
def features(item: Type[HomeownerProtocol]) -> Type[Homeowner]: ...

@overload
def features(item: Type[ETLFeaturesProtocol]) -> Type[ETLFeatures]: ...

@overload
def features(item: Type[ChildFSProtocol]) -> Type[ChildFS]: ...

@overload
def features(item: Type[UnassignedIdFeaturesProtocol]) -> Type[UnassignedIdFeatures]: ...

@overload
def features(item: Type[UnassignedDecoratedIdFeaturesProtocol]) -> Type[UnassignedDecoratedIdFeatures]: ...

@overload
def features(item: Type[TheArtistFormerlyKnownAsPrinceProtocol]) -> Type[TheArtistFormerlyKnownAsPrince]: ...

@overload
def features(item: Type[StreamFeaturesWindowProtocol]) -> Type[StreamFeaturesWindow]: ...

@overload
def features(item: Type[SingleParentFSProtocol]) -> Type[SingleParentFS]: ...

@overload
def features(item: Type[SingleChildFSProtocol]) -> Type[SingleChildFS]: ...

@overload
def features(item: Type[SQLUserFeaturesProtocol]) -> Type[SQLUserFeatures]: ...

@overload
def features(item: Type[NotIdIsIdFeaturesProtocol]) -> Type[NotIdIsIdFeatures]: ...

@overload
def features(item: Type[IdIsNotIdFeaturesProtocol]) -> Type[IdIsNotIdFeatures]: ...

@overload
def features(item: Type[ExplicitIdFeaturesProtocol]) -> Type[ExplicitIdFeatures]: ...

@overload
def features(item: Type[ExampleFraudUserProtocol]) -> Type[ExampleFraudUser]: ...

@overload
def features(item: Type[ExampleFraudProfileProtocol]) -> Type[ExampleFraudProfile]: ...

@overload
def features(item: Type[ExampleFraudOrgProtocol]) -> Type[ExampleFraudOrg]: ...

@overload
def features(item: Type[CustomNameClassProtocol]) -> Type[CustomNameClass]: ...

@overload
def features(item: Type[BogusIdFeature3Protocol]) -> Type[BogusIdFeature3]: ...

@overload
def features(item: Type[BogusIdFeature2Protocol]) -> Type[BogusIdFeature2]: ...

@overload
def features(item: Type[BogusIdFeature1Protocol]) -> Type[BogusIdFeature1]: ...

@overload
def features(item: Type[AnkleProtocol]) -> Type[Ankle]: ...

@overload
def features(item: Type[AcctProtocol]) -> Type[Acct]: ...

@overload
def features(item: Type[AccountProtocol]) -> Type[Account]: ...

@overload
def features(item: Type[UserFeaturesProtocol]) -> Type[UserFeatures]: ...

@overload
def features(item: Type[StreamFeaturesProtocol]) -> Type[StreamFeatures]: ...

@overload
def features(item: Type[NoFunFeaturesProtocol]) -> Type[NoFunFeatures]: ...

@overload
def features(item: Type[NicknameProtocol]) -> Type[Nickname]: ...

@overload
def features(item: Type[LibraryFeaturesProtocol]) -> Type[LibraryFeatures]: ...

@overload
def features(item: Type[FeaturesClassWithNamedTsProtocol]) -> Type[FeaturesClassWithNamedTs]: ...

@overload
def features(item: Type[FeaturesClassWithCustomTsNameProtocol]) -> Type[FeaturesClassWithCustomTsName]: ...

@overload
def features(item: Type[FeaturesClassWithoutTimestampProtocol]) -> Type[FeaturesClassWithoutTimestamp]: ...

@overload
def features(
    *,
    owner: Optional[str] = ...,
    tags: Optional[Tags] = ...,
    max_staleness: Optional[Duration] = ...,
    etl_offline_to_online: Optional[bool] = ...,
) -> __stubgen__features_proto: ...

class __stubgen__features_proto(Protocol):
    @overload
    def __call__(self, item: Type[WowFSProtocol]) -> Type[WowFS]: ...

    @overload
    def __call__(self, item: Type[TacoProtocol]) -> Type[Taco]: ...

    @overload
    def __call__(self, item: Type[HelloProtocol]) -> Type[Hello]: ...

    @overload
    def __call__(self, item: Type[MappingFeaturesProtocol]) -> Type[MappingFeatures]: ...

    @overload
    def __call__(self, item: Type[CommentBaseOwnerProtocol]) -> Type[CommentBaseOwner]: ...

    @overload
    def __call__(self, item: Type[ToppingProtocol]) -> Type[Topping]: ...

    @overload
    def __call__(self, item: Type[PersonProtocol]) -> Type[Person]: ...

    @overload
    def __call__(self, item: Type[HomeFeaturesChainedFeatureTimeProtocol]) -> Type[HomeFeaturesChainedFeatureTime]: ...

    @overload
    def __call__(self, item: Type[FootProtocol]) -> Type[Foot]: ...

    @overload
    def __call__(self, item: Type[TransactionProtocol]) -> Type[Transaction]: ...

    @overload
    def __call__(self, item: Type[ToppingPriceProtocol]) -> Type[ToppingPrice]: ...

    @overload
    def __call__(self, item: Type[TagFeaturesProtocol]) -> Type[TagFeatures]: ...

    @overload
    def __call__(self, item: Type[ParentFSProtocol]) -> Type[ParentFS]: ...

    @overload
    def __call__(self, item: Type[OwnerFeaturesProtocol]) -> Type[OwnerFeatures]: ...

    @overload
    def __call__(self, item: Type[MypyUserFeaturesProtocol]) -> Type[MypyUserFeatures]: ...

    @overload
    def __call__(self, item: Type[HomeFeaturesProtocol]) -> Type[HomeFeatures]: ...

    @overload
    def __call__(self, item: Type[FunFeaturesProtocol]) -> Type[FunFeatures]: ...

    @overload
    def __call__(self, item: Type[UserProfileProtocol]) -> Type[UserProfile]: ...

    @overload
    def __call__(self, item: Type[UserProtocol]) -> Type[User]: ...

    @overload
    def __call__(self, item: Type[SQLFriendsWithRowProtocol]) -> Type[SQLFriendsWithRow]: ...

    @overload
    def __call__(self, item: Type[OtherPrimaryKeyFeaturesProtocol]) -> Type[OtherPrimaryKeyFeatures]: ...

    @overload
    def __call__(self, item: Type[MaxStalenessFeaturesProtocol]) -> Type[MaxStalenessFeatures]: ...

    @overload
    def __call__(self, item: Type[HomeownerProtocol]) -> Type[Homeowner]: ...

    @overload
    def __call__(self, item: Type[ETLFeaturesProtocol]) -> Type[ETLFeatures]: ...

    @overload
    def __call__(self, item: Type[ChildFSProtocol]) -> Type[ChildFS]: ...

    @overload
    def __call__(self, item: Type[UnassignedIdFeaturesProtocol]) -> Type[UnassignedIdFeatures]: ...

    @overload
    def __call__(self, item: Type[UnassignedDecoratedIdFeaturesProtocol]) -> Type[UnassignedDecoratedIdFeatures]: ...

    @overload
    def __call__(self, item: Type[TheArtistFormerlyKnownAsPrinceProtocol]) -> Type[TheArtistFormerlyKnownAsPrince]: ...

    @overload
    def __call__(self, item: Type[StreamFeaturesWindowProtocol]) -> Type[StreamFeaturesWindow]: ...

    @overload
    def __call__(self, item: Type[SingleParentFSProtocol]) -> Type[SingleParentFS]: ...

    @overload
    def __call__(self, item: Type[SingleChildFSProtocol]) -> Type[SingleChildFS]: ...

    @overload
    def __call__(self, item: Type[SQLUserFeaturesProtocol]) -> Type[SQLUserFeatures]: ...

    @overload
    def __call__(self, item: Type[NotIdIsIdFeaturesProtocol]) -> Type[NotIdIsIdFeatures]: ...

    @overload
    def __call__(self, item: Type[IdIsNotIdFeaturesProtocol]) -> Type[IdIsNotIdFeatures]: ...

    @overload
    def __call__(self, item: Type[ExplicitIdFeaturesProtocol]) -> Type[ExplicitIdFeatures]: ...

    @overload
    def __call__(self, item: Type[ExampleFraudUserProtocol]) -> Type[ExampleFraudUser]: ...

    @overload
    def __call__(self, item: Type[ExampleFraudProfileProtocol]) -> Type[ExampleFraudProfile]: ...

    @overload
    def __call__(self, item: Type[ExampleFraudOrgProtocol]) -> Type[ExampleFraudOrg]: ...

    @overload
    def __call__(self, item: Type[CustomNameClassProtocol]) -> Type[CustomNameClass]: ...

    @overload
    def __call__(self, item: Type[BogusIdFeature3Protocol]) -> Type[BogusIdFeature3]: ...

    @overload
    def __call__(self, item: Type[BogusIdFeature2Protocol]) -> Type[BogusIdFeature2]: ...

    @overload
    def __call__(self, item: Type[BogusIdFeature1Protocol]) -> Type[BogusIdFeature1]: ...

    @overload
    def __call__(self, item: Type[AnkleProtocol]) -> Type[Ankle]: ...

    @overload
    def __call__(self, item: Type[AcctProtocol]) -> Type[Acct]: ...

    @overload
    def __call__(self, item: Type[AccountProtocol]) -> Type[Account]: ...

    @overload
    def __call__(self, item: Type[UserFeaturesProtocol]) -> Type[UserFeatures]: ...

    @overload
    def __call__(self, item: Type[StreamFeaturesProtocol]) -> Type[StreamFeatures]: ...

    @overload
    def __call__(self, item: Type[NoFunFeaturesProtocol]) -> Type[NoFunFeatures]: ...

    @overload
    def __call__(self, item: Type[NicknameProtocol]) -> Type[Nickname]: ...

    @overload
    def __call__(self, item: Type[LibraryFeaturesProtocol]) -> Type[LibraryFeatures]: ...

    @overload
    def __call__(self, item: Type[FeaturesClassWithNamedTsProtocol]) -> Type[FeaturesClassWithNamedTs]: ...

    @overload
    def __call__(self, item: Type[FeaturesClassWithCustomTsNameProtocol]) -> Type[FeaturesClassWithCustomTsName]: ...

    @overload
    def __call__(self, item: Type[FeaturesClassWithoutTimestampProtocol]) -> Type[FeaturesClassWithoutTimestamp]: ...
