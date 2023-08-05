# -*- coding: utf-8 -*-
from graphene_django_crud import DjangoCRUDObjectType
import graphene
from .models import *


class TestFkAType(DjangoCRUDObjectType):
    class Meta:
        model = TestFkA


class TestFkBType(DjangoCRUDObjectType):
    class Meta:
        model = TestFkB


class TestFkCType(DjangoCRUDObjectType):
    class Meta:
        model = TestFkC


class TestO2oAType(DjangoCRUDObjectType):
    class Meta:
        model = TestO2oA


class TestO2oBType(DjangoCRUDObjectType):
    class Meta:
        model = TestO2oB


class TestO2oCType(DjangoCRUDObjectType):
    class Meta:
        model = TestO2oC


class TestM2mAType(DjangoCRUDObjectType):
    class Meta:
        model = TestM2mA


class TestM2mBType(DjangoCRUDObjectType):
    class Meta:
        model = TestM2mB


class TestM2mCType(DjangoCRUDObjectType):
    class Meta:
        model = TestM2mC


class PersonType(DjangoCRUDObjectType):
    class Meta:
        model = Person


class Query(graphene.ObjectType):

    test_fk_a = TestFkAType.ReadField()
    test_fk_as = TestFkAType.BatchReadField()

    test_fk_b = TestFkBType.ReadField()
    test_fk_bs = TestFkBType.BatchReadField()

    test_fk_c = TestFkCType.ReadField()
    test_fk_cs = TestFkCType.BatchReadField()

    test_o2o_a = TestO2oAType.ReadField()
    test_o2o_as = TestO2oAType.BatchReadField()

    test_o2o_b = TestO2oBType.ReadField()
    test_o2o_bs = TestO2oBType.BatchReadField()

    test_o2o_c = TestO2oCType.ReadField()
    test_o2o_cs = TestO2oCType.BatchReadField()

    test_m2m_a = TestM2mAType.ReadField()
    test_m2m_as = TestM2mAType.BatchReadField()

    test_m2m_b = TestM2mBType.ReadField()
    test_m2m_bs = TestM2mBType.BatchReadField()

    test_m2m_c = TestM2mCType.ReadField()
    test_m2m_cs = TestM2mCType.BatchReadField()

    person = PersonType.ReadField()
    persons = PersonType.BatchReadField()


class Mutation(graphene.ObjectType):

    test_fk_a_create = TestFkAType.CreateField()
    test_fk_a_update = TestFkAType.UpdateField()
    test_fk_a_delete = TestFkAType.DeleteField()

    test_fk_b_create = TestFkBType.CreateField()
    test_fk_b_update = TestFkBType.UpdateField()
    test_fk_b_delete = TestFkBType.DeleteField()

    test_fk_c_create = TestFkCType.CreateField()
    test_fk_c_update = TestFkCType.UpdateField()
    test_fk_c_delete = TestFkCType.DeleteField()

    test_o2o_a_create = TestO2oAType.CreateField()
    test_o2o_a_update = TestO2oAType.UpdateField()
    test_o2o_a_delete = TestO2oAType.DeleteField()

    test_o2o_b_create = TestO2oBType.CreateField()
    test_o2o_b_update = TestO2oBType.UpdateField()
    test_o2o_b_delete = TestO2oBType.DeleteField()

    test_o2o_c_create = TestO2oCType.CreateField()
    test_o2o_c_update = TestO2oCType.UpdateField()
    test_o2o_c_delete = TestO2oCType.DeleteField()

    test_m2m_a_create = TestM2mAType.CreateField()
    test_m2m_a_update = TestM2mAType.UpdateField()
    test_m2m_a_delete = TestM2mAType.DeleteField()

    test_m2m_b_create = TestM2mBType.CreateField()
    test_m2m_b_update = TestM2mBType.UpdateField()
    test_m2m_b_delete = TestM2mBType.DeleteField()

    test_m2m_c_create = TestM2mCType.CreateField()
    test_m2m_c_update = TestM2mCType.UpdateField()
    test_m2m_c_delete = TestM2mCType.DeleteField()

    person_create = PersonType.CreateField()
    person_update = PersonType.UpdateField()
    person_delete = PersonType.DeleteField()


class Subscription(graphene.ObjectType):

    test_fk_a_created = TestFkAType.CreatedField()
    test_fk_a_updated = TestFkAType.UpdatedField()
    test_fk_a_deleted = TestFkAType.DeletedField()

    test_fk_b_created = TestFkBType.CreatedField()
    test_fk_b_updated = TestFkBType.UpdatedField()
    test_fk_b_deleted = TestFkBType.DeletedField()

    test_fk_c_created = TestFkCType.CreatedField()
    test_fk_c_updated = TestFkCType.UpdatedField()
    test_fk_c_deleted = TestFkCType.DeletedField()

    test_o2o_a_created = TestO2oAType.CreatedField()
    test_o2o_a_updated = TestO2oAType.UpdatedField()
    test_o2o_a_deleted = TestO2oAType.DeletedField()

    test_o2o_b_created = TestO2oBType.CreatedField()
    test_o2o_b_updated = TestO2oBType.UpdatedField()
    test_o2o_b_deleted = TestO2oBType.DeletedField()

    test_o2o_c_created = TestO2oCType.CreatedField()
    test_o2o_c_updated = TestO2oCType.UpdatedField()
    test_o2o_c_deleted = TestO2oCType.DeletedField()

    test_m2m_a_created = TestM2mAType.CreatedField()
    test_m2m_a_updated = TestM2mAType.UpdatedField()
    test_m2m_a_deleted = TestM2mAType.DeletedField()

    test_m2m_b_created = TestM2mBType.CreatedField()
    test_m2m_b_updated = TestM2mBType.UpdatedField()
    test_m2m_b_deleted = TestM2mBType.DeletedField()

    test_m2m_c_created = TestM2mCType.CreatedField()
    test_m2m_c_updated = TestM2mCType.UpdatedField()
    test_m2m_c_deleted = TestM2mCType.DeletedField()

    person_created = PersonType.CreatedField()
    person_updated = PersonType.UpdatedField()
    person_deleted = PersonType.DeletedField()
