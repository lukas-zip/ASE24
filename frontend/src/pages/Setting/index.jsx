import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { createNewExpenseCategory, deleteAllData, deleteExpenseCategory, exportAllData, getAllExpenseCategory, updateExpenseCategory } from '../../api/setting.api'
import { Button, Card, Col, Input, List, Modal, Popconfirm, Radio, Row, Switch, Typography, message } from 'antd'
import { DeleteOutlined, EditOutlined, ExportOutlined, PlusOutlined } from '@ant-design/icons'
import useUserTheme from '../../hooks/useUserTheme'
import { setUserTheme } from '../../store/user.store'


const themeOptions = [
    {
        label: 'Light',
        value: 'light',
    },
    {
        label: 'Dark',
        value: 'dark',
    },
];


function Setting() {
    const { user } = useSelector(state => state.user)
    const [allCategories, setAllCategories] = useState([])
    const getAllCategory = async () => {
        await getAllExpenseCategory(user.id).then(res => {
            if (res && res.status !== false) {
                setAllCategories(res)
            }
        })
    }
    const deleteCategory = async (id) => {
        await deleteExpenseCategory(id).then(res => {
            if (res && res.status !== false) {
                getAllCategory()
            }
        })
    }

    const addNewCategory = async () => {
        const data = { category_name: categoryName, user_id: user.id }
        await createNewExpenseCategory(data).then(res => {
            if (res && res.status !== false) {
                setCategoryName('')
                setAddModalOpen(false)
                getAllCategory()
            }
        })
    }
    useEffect(() => {
        getAllCategory()
    }, [])
    const [addModalOpen, setAddModalOpen] = useState(false)
    const [updateModalOpen, setUpdateModalOpen] = useState(false)
    const [selectedCategory, setselectedCategory] = useState()
    const [categoryName, setCategoryName] = useState('')
    const dispatch = useDispatch()
    const currentTheme = useUserTheme()

    const handleExport = async () => {
        await exportAllData(user.id).then(res => {
            if (res && res.status !== false) {
                message.success('Exported successfully at "Downloads/"')
            }
        })
    }
    const handleDeleteAll = async () => {
        await deleteAllData(user.id).then(res => {
            if (res && res.status !== false) {
                message.success('Delete Succuessfully')
            }
        })
    }
    return (
        <div>
            <Card bodyStyle={{ padding: 0 }}>
                <List
                    header={
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <h4>All Category Name ({allCategories.length} categories)</h4>
                            <Button onClick={() => setAddModalOpen(true)}><PlusOutlined />Add</Button>
                        </div>
                    }
                    footer={null}
                    bordered
                    dataSource={allCategories}
                    renderItem={(item) => (
                        <List.Item>
                            <div style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                                <div>
                                    {item.category_name}
                                </div>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                                    <div
                                        className='hoverButton'
                                        onClick={() => {
                                            setselectedCategory(item)
                                            setUpdateModalOpen(true)
                                        }}>
                                        <EditOutlined />
                                    </div>
                                    <Popconfirm
                                        title="Delete"
                                        description="Are you sure to delete this category?"
                                        onConfirm={() => deleteCategory(item.id)}
                                        onCancel={() => { }}
                                        okText="Yes"
                                        cancelText="No"
                                    >
                                        <div className='hoverButton'>
                                            <DeleteOutlined />
                                        </div>
                                    </Popconfirm>
                                </div>
                            </div>
                        </List.Item>
                    )}
                />
            </Card>

            <Row gutter={8}>
                <Col span={8}>
                    <Card>
                        <div className='hoverButton' onClick={() => handleExport()}><ExportOutlined /> Export Data</div>
                    </Card>
                </Col>
                <Col span={8}>
                    <Popconfirm
                        title="Delete"
                        description="Are you sure to delete all your data?"
                        onConfirm={() => handleDeleteAll()}
                        onCancel={() => { }}
                        okText="Yes"
                        cancelText="No"
                    >
                        <Card>
                            <div className='hoverButton'><DeleteOutlined /> Delete All Data</div>
                        </Card>
                    </Popconfirm>
                </Col>
                <Col span={8}>
                    <Card>
                        <Radio.Group options={themeOptions} onChange={({ target: { value } }) => { dispatch(setUserTheme(value)) }} value={currentTheme} />
                    </Card>
                </Col>
            </Row>
            <Modal
                footer={null}
                title={"Add New Category"}
                open={addModalOpen}
                onCancel={() => setAddModalOpen(false)}
                onOk={() => setAddModalOpen(false)}
            >
                <div style={{ paddingTop: 10, display: 'flex', alignItems: 'center', gap: 10 }}>
                    <div style={{ width: 160 }}>
                        Category Name:
                    </div>
                    <Input placeholder="Input Category Name" value={categoryName} onChange={(e) => setCategoryName(e.target.value)} />
                </div>
                <div style={{ marginTop: 10, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Button onClick={addNewCategory} type='primary'>Add</Button>
                </div>
            </Modal>
            <UpdateCategoryModal refresh={getAllCategory} open={updateModalOpen} setOpen={setUpdateModalOpen} selectedCategory={selectedCategory} />
        </div >
    )
}

const UpdateCategoryModal = ({ open, setOpen, selectedCategory, refresh }) => {
    const { user } = useSelector(state => state.user)
    const [updatedCategoryName, setUpdatedCategoryName] = useState(selectedCategory?.category_name)
    useEffect(() => {
        selectedCategory?.category_name && setUpdatedCategoryName(selectedCategory.category_name)
    }, [selectedCategory?.category_name])
    const updateCategory = async () => {
        if (updatedCategoryName) {
            const data = { category_name: updatedCategoryName, user_id: user.id }
            await updateExpenseCategory(selectedCategory.id, data).then(res => {
                if (res && res.status !== false) {
                    setOpen(false)
                    refresh()
                }
            })
        } else {
            message.error("Please input the category name")
        }
    }
    return <Modal
        footer={null}
        title={"Update The Category"}
        open={open}
        onCancel={() => setOpen(false)}
        onOk={() => setOpen(false)}
    >
        <div style={{ paddingTop: 10, display: 'flex', alignItems: 'center', gap: 10 }}>
            <div style={{ width: 160 }}>
                Category Name:
            </div>
            <Input placeholder="Input Category Name" value={updatedCategoryName} onChange={(e) => setUpdatedCategoryName(e.target.value)} />
        </div>
        <div style={{ marginTop: 10, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Button onClick={() => updateCategory()} type='primary'>Update</Button>
        </div>
    </Modal>
}

export default Setting