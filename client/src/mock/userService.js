import Mock from 'mockjs';

// 模拟用户注册
Mock.mock('/users', 'post', {
    'status': true,
    'value': {
        'address': 'Test Street, Zuerich 00000',
        'email': '666666.me@example.com',
        'phone': '234312424',
        'profile_picture': 'NONE',
        'type': 'User',
        'user_id': '@guid',
        'username': 'test',
    }
});

// 模拟商店注册
Mock.mock('/shops', 'post', {
    'status': true,
    'value': {
        'address': 'Selfmade 19, Bern',
        'description': 'My hanyshop, wher I make sustainable goods.',
        'email': 'selfmade@example.com',
        'phone': '32508990235',
        'profile_picture': 'NONE',
        'shop_id': '@guid',
        'shop_name': 'Selfmade',
        'type': 'Shop',
    }
});

// 模拟用户登录
Mock.mock(RegExp('/users' + '.*'), 'post', {
    'status': true,
    'value': {
        'address': 'Hoferstrasse 19, Zuerich',
        'email': 'micro@example.com',
        'phone': '1234567890',
        'profile_picture': 'NONE',
        'user_id': '@guid',
        'username': 'John Micro',
        'type': 'User',
    }
});

// 模拟商店登录
Mock.mock(RegExp('/shops' + '.*'), 'post', {
    'status': true,
    'value': {
        'address': 'Hoferstrasse 19, Zuerich',
        'description': 'My small handcraft shop.',
        'email': 'micro@example.com',
        'phone': '1234567890',
        'profile_picture': 'NONE',
        'shop_id': '@guid',
        'shop_name': 'John Micro',
        'type': 'Shop',
    }
});

// 模拟更新实体数据
Mock.mock(RegExp('/users/\\w+|/shops/\\w+' + '.*'), 'put', {
    'status': true,
    'value': {
        'address': 'update Street, Zuerich',
        'email': 'update@example.com',
        'phone': '324314332414',
        'profile_picture': 'NONE',
        'shop_id': '@guid',
        'shop_name': 'update Hydro',
        'type': '@pick(["User", "Shop"])',
        'user_id': '@guid',
        'username': 'update',
    }
});

// 模拟获取实体信息
Mock.mock(RegExp('/users/\\w+|/shops/\\w+'), 'get', {
    'status': true,
    'value': {
        'address': 'update Street, Zuerich',
        'description': null,
        'email': 'hi.me@example.com',
        'phone': '234312424',
        'profile_picture': 'http://userview.s3.localhost.localstack.cloud:4566/a0b76086-feb5-4240-aab1-8351b820c30a/profile_picture.png',
        'shop_id': '@guid',
        'shop_name': null,
        'type': 'User',
    }
});

// 模拟删除实体
Mock.mock(RegExp('/users/\\w+|/shops/\\w+'), 'delete', {
    'status': true,
    'value': 'Deleted successfully',
});

// 注意: 在Mock.mock的URL参数中使用RegExp是为了支持动态的user_id和shop_id。
// '@guid'是Mockjs提供的一个用于生成GUID的占位符。
