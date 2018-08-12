#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18/8/11 11:51
# @Author  : Medivh


from asset import models
import json
from asset.ext import db


class AssetDashboard(object):
    '''首页画图需要的数据都在这里生产'''

    def __init__(self, reqeust):
        self.requeset = reqeust
        self.asset_list = models.Asset.query.all()
        self.data = {}

    def searilize_page(self):
        '''生成页面需要的数据'''
        self.data['asset_categories'] = self.get_asset_categories()
        self.data['asset_status_list'] = self.get_asset_status_statistics()
        self.data['business_load'] = self.get_business_load()
        # print('data',self.data)
        return self.data

    def get_business_load(self):
        '''调用监控等系统，得到每个业务线的负载率'''

        dataset = {
            'names': [],
            'data': {'load': [], 'left': []}  # left是为了填充百分比用的
        }
        load_list = []
        for obj in models.BusinessUnit.query.all():
            queryset = db.session.query(models.Asset).filter_by(business_unit=obj.name).all()
            for i in queryset:
                memory = eval(i.memory)
                load_val = memory['percent']
                load_list.append(load_val)
            load_val = int(sum(load_list) / len(load_list))
            dataset['names'].append(obj.name)
            dataset['data']['load'].append(load_val)
            dataset['data']['left'].append(100 - load_val)
        return dataset

    def get_asset_status_statistics(self):

        '''资产状态分类统计'''
        queryset = db.session.query(models.Asset.status, db.func.count('*').label("status")).group_by(
                models.Asset.status).all()
        dataset = {
            'names': [],
            'data': []
        }
        new = []
        names = []
        for i in queryset:
            s1 = {}
            if i[0] == 'RUN':
                s1['itemStyle'] = {
                    'normal': {'color': 'yellowgreen'}
                }
            s1['name'] = i[0]
            names.append(i[0])
            s1['value'] = i[1]
            new.append(s1)

        dataset['names'] = names
        dataset['data'] = new
        return dataset

    def get_asset_categories(self):

        '''资产状态分类统计'''
        queryset = db.session.query(models.Asset.type, db.func.count('*').label("status")).group_by(
                models.Asset.type).all()
        dataset = {
            'names': [],
            'data': []
        }
        new = []
        names = []
        for i in queryset:
            s1 = {}
            s1['name'] = i[0]
            names.append(i[0])
            s1['value'] = i[1]
            new.append(s1)

        dataset['names'] = names
        dataset['data'] = new
        return dataset
