import { Avatar, Button, Form, Input, Modal, Popover, message } from 'antd'
import { Header } from 'antd/es/layout/layout'
import './index.less'
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { setUser } from '../../store/user.store';
import useUserTheme from '../../hooks/useUserTheme';
import COLORS from '../../constants/COLORS';
// import { updatePassword } from '../../api/user.api';
import { useRef, useState } from 'react';
import PROJECT_VARIABLE from '../../constants/ProjectNameVariable';

export default function MyLayoutHeader() {
    // const { user: { id, name, email } } = useSelector(state => state.user)
    const id = 1
    const name = "leon"
    const email = "leon@qq.com"
    const dispatch = useDispatch()
    const navigateTo = useNavigate()
    const loginStatusDiv = (
        <div style={{ display: "grid", gridTemplateColumns: 'auto' }}>
            <Button
                danger
                className='hoverButton'
                onClick={() => {
                    dispatch(setUser(null))
                    navigateTo('/login')
                }}
            >
                Logout
            </Button>
        </div>
    );
    const [updatePasswordModelOpen, setUpdatePasswordModelOpen] = useState(false)
    const handleUpdate = async (values) => {
        const { updatedPassword } = values
        console.log("updatedPassword", updatedPassword);
        if (updatedPassword && updatedPassword.length > 5) {
            const req = { email, password: updatedPassword }
            // await updatePassword(id, req).then(res => {
            //     if (res && res.status !== false) {
            //         message.success("Update password successfully!")
            //         // dispatch(setUser(res))
            //         setUpdatePasswordModelOpen(false)
            //         form.resetFields();
            //     } else {
            //         message.error("error")
            //     }
            // })
        } else {
            message.error("Please input the password, and password must be greater than 5 chars")
        }
    }
    const theme = useUserTheme()
    const [form] = Form.useForm()
    return (
        <Header className='layout-page-header' style={theme === "light" ? { boxShadow: '0 4px 10px #dddddd', backgroundColor: COLORS.white } : {}}>
            <div className='layout-page-header-left'>
                <div className="medal-logo">{PROJECT_VARIABLE.PROJECT_NAME}</div>
            </div>
            <div className='layout-page-header-right'>
                <Popover placement="bottom" content={loginStatusDiv} trigger="click">
                    <Avatar className='MyHeader-Avatar' size="large">{name}</Avatar>
                </Popover>
            </div>
            <Modal
                open={updatePasswordModelOpen}
                onCancel={() => setUpdatePasswordModelOpen(false)}
                onOk={() => setUpdatePasswordModelOpen(false)}
                title={"Create Budget"}
                footer={null}
            >
                <Form
                    form={form}
                    onFinish={handleUpdate}
                    labelCol={{ span: 8, }}
                    wrapperCol={{ span: 16, }}
                    style={{ maxWidth: 600, }}
                    autoComplete="off"
                >
                    <Form.Item label="New Password" name="updatedPassword"
                        rules={[{ required: true, message: 'Please input budget name!', }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item wrapperCol={{ offset: 8, span: 16, }}>
                        <Button type="primary" htmlType="submit">
                            Update
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </Header>
    )
}
