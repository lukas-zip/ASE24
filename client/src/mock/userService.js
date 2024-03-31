import Mock from 'mockjs'

Mock.mock("/user/register", "POST", {
    value: {
        address: "Hoferstrasse 19, Zuerich",
        description: "My small handcraft shop.",
        email: "micro@example.com",
        phone: "1234567890",
        profile_picture: "NONE",
        user_id: "0638fad3-26f8-473a-9b54-6b5fb4ae7e0f",
        username: "John Micro",
        type: "User"
    },
    status: true
})

Mock.mock("/shop/register", "POST", {
    value: {
        address: "Hoferstrasse 19, Zuerich",
        description: "My small handcraft shop.",
        email: "micro@example.com",
        phone: "1234567890",
        profile_picture: "NONE",
        shop_id: "0638fad3-26f8-473a-9b54-6b5fb4ae7e0f",
        shop_name: "John Micro",
        type: "Shop"
    },
    status: true
})
Mock.mock("/login", "post", {
    value: {
        address: "Hoferstrasse 19, Zuerich",
        description: "My small handcraft shop.",
        email: "micro@example.com",
        phone: "1234567890",
        profile_picture: "NONE",
        user_id: "0638fad3-26f8-473a-9b54-6b5fb4ae7e0f",
        username: "John Micro",
        type: "User"
    },
    status: true
})
Mock.mock("/update/<entity_uui", "PUT", {})
Mock.mock("/password/<entity_u", "PUT", {})
Mock.mock("/profilepicture/<en", "PUT", {})
Mock.mock("/get/<entity_uuid>", "GET", {})
Mock.mock("/delete/<entity_id>", "DELETE", {})