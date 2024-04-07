import Mock from 'mockjs';

// 模拟用户登录
Mock.mock(/\/login$/, 'post', {
    'status': true,
    'value': {
        'address': 'Hoferstrasse 19, Zuerich',
        'email': 'micro@example.com',
        'phone': '1234567890',
        'profile_picture': 'NONE',
        'user_id': '4321',
        'username': 'John Micro',
        'type': 'User',
    }
});



// 模拟用户注册
Mock.mock(/\/users$/, 'post', {
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

Mock.mock(/\/shops$/, 'post', {
    'status': true,
    'value': {
        'address': 'Test Street, Zuerich 00000',
        'email': '666666.me@example.com',
        'phone': '234312424',
        'profile_picture': 'NONE',
        'type': 'Shop',
        'shop_id': '@guid',
        'shop_name': 'test',
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


Mock.mock(/\/review$/, 'post', {
    'status': true,
    'value': {
        "value": "Review deleted successfully",
        "status": true
    }
});
Mock.mock(/\/review\/([a-zA-Z0-9-]+)$/, 'get', {
    "status": true,
    "value": [
        {
            "customer_id": "43210",
            "product_id": "1234",
            "rating": "4",
            "review_id": "Review#a2cc92c2-02af-4bd6-ae00-38ead471a490",
            "reviewcontent": "Greate Design",
            "time_created": "20.03.2024 - 11:50:00",
            "time_lastedit": "20.03.2024 - 11:50:00"
        },
        {
            "customer_id": "4321",
            "product_id": "1234",
            "rating": "4",
            "review_id": "Review#92be4046-55f3-47c3-a903-2f52beed3a4b",
            "reviewcontent": "Greate Design",
            "time_created": "20.03.2024 - 11:50:00",
            "time_lastedit": "20.03.2024 - 11:50:00"
        }
    ]
});


Mock.mock(/\/product\/cataloguesell\/([a-zA-Z0-9-]+)$/, 'get', {
    "status": true,
    "value": [
        {
            "product_assemblies": "Final",
            "product_bom": [
                "1324a686-c8b1-4c84-bbd6-17325209d78c1",
                "1324a686-c8b1-4c84-bbd6-17325209d78c2"
            ],
            "product_category": [
                ""
            ],
            "product_current_stock": "0",
            "product_description": "exampleDescription",
            "product_id": "ec6e7ae8-7456-4928-bdcf-0e2d0fe47521",
            "product_name": "exampleProduct",
            "product_owner": "1324a686-c8b1-4c84-bbd6-17325209d78c6",
            "product_picture": "http://localhost:4566/productpictures/ec6e7ae8-7456-4928-bdcf-0e2d0fe47521.jpg",
            "product_price": "0",
            "product_price_reduction": "0",
            "product_reviews": [
                "thiswouldbeanid"
            ],
            "product_sale": false,
            "product_search_attributes": [
                "black",
                "curled"
            ],
            "product_should_stock": "0"
        },
        {
            "product_assemblies": "Final",
            "product_bom": [
                "1324a686-c8b1-4c84-bbd6-17325209d78c1",
                "1324a686-c8b1-4c84-bbd6-17325209d78c2"
            ],
            "product_category": [
                "ThiswouldbeanID"
            ],
            "product_current_stock": "0",
            "product_description": "exampleDescription",
            "product_id": "e3e35506-b554-4b3b-9111-79818ea56ea8",
            "product_name": "anotherSELLProduct",
            "product_owner": "1324a686-c8b1-4c84-bbd6-17325209d78c6",
            "product_picture": "http://localhost:4566/productpictures/e3e35506-b554-4b3b-9111-79818ea56ea8.jpg",
            "product_price": "0",
            "product_price_reduction": "0",
            "product_reviews": [
                "thiswouldbeanid"
            ],
            "product_sale": false,
            "product_search_attributes": [
                "black",
                "curled"
            ],
            "product_should_stock": "0"
        }
    ]
})