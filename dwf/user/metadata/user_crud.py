# -*- coding:utf-8 -*-
#
# DataWay Dataset SDK
# Initial Date: 2019.06.21
#
# Title: methods for metadata of user
#
# Version 0.1
#

from dwf.common.exception import *
from dwf.common.log import logger
from dwf.ormmodels import User, datetime
from dwf.util.id import generate_primary_key


class UserCRUD:

    def __init__(self, db_session):
        self.db_session = db_session

    def add_user(
            self,
            name,
            date=None,
            creator=None,
            subid=None,
            last_modifier=None,
            last_modify_time=None,
            comment=None,
            password=None,
            display_name=None,
            email=None,
            expiredtime=None,
            isfrozen=False):
        """

        :param name:
        :param date:
        :param creator:
        :param subid:
        :param last_modifier:
        :param last_modify_time:
        :param comment:
        :param password:
        :param display_name:
        :param email:
        :param expiredtime:
        :param isfrozen:
        :return:
        """

        id = generate_primary_key('USER')
        create_time = datetime.now()

        if creator is None:
            creator = 'admin'
        if last_modifier is None:
            last_modifier = 'admin'

        user = User(
            id=id,
            date=date,
            creator=creator,
            subid=subid,
            last_modifier=last_modifier,
            last_modify_time=last_modify_time,
            comment=comment,
            name=name,
            password=password,
            create_time=create_time,
            display_name=display_name,
            email=email,
            expiredtime=expiredtime,
            isfrozen=isfrozen)
        self.db_session.add(user)
        self.db_session.commit()

        return id

    def get_user(self, user_id):
        """
        通过ID获取数据集元信息

        :param dataset_id: 数据集ID
        :return: 数据集元信息
        """

        user = self.db_session.query(User).get(user_id)

        return user

    def get_all_user(self):
        """
        获取全部的数据集元信息

        :return: 数据集元信息列表
        """

        user_list = self.db_session.query(User).all()

        return user_list

    def delete_user(self, user_id):
        """
        删除数据集元信息

        :param dataset_id: 数据集ID
        :return: 无
        """

        user = self.db_session.query(User).get(user_id)
        self.db_session.delete(user)
        self.db_session.commit()

    def update_user(
            self,
            user_id,
            name=None,
            date=None,
            creator=None,
            subid=None,
            last_modifier=None,
            comment=None,
            password=None,
            display_name=None,
            email=None,
            expiredtime=None,
            isfrozen=False):
        """

        :param user_id:
        :param name:
        :param date:
        :param creator:
        :param subid:
        :param last_modifier:
        :param last_modify_time:
        :param comment:
        :param password:
        :param display_name:
        :param email:
        :param expiredtime:
        :param isfrozen:
        :return:
        """

        if user_id is None:
            logger.error('缺少数据集ID')
            raise PARAM_LACK

        user = self.db_session.query(User).get(user_id)

        if name is not None:
            user.name = name
        if date is not None:
            user.date = date
        if creator is not None:
            user.creator = creator
        if subid is not None:
            user.subid = subid
        if last_modifier is not None:
            user.last_modifier = last_modifier
        if comment is not None:
            user.comment = comment
        if password is not None:
            user.password = password
        if display_name is not None:
            user.display_name = display_name
        if email is not None:
            user.email = email
        if expiredtime is not None:
            user.expiredtime = expiredtime
        if isfrozen is not None:
            user.isfrozen = isfrozen

        user.last_modify_time = datetime.now()
        self.db_session.commit()
