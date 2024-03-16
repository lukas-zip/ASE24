import React, { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'
import { getExpenseCategories, getSavingByUserID, getSavingTotalByCategories } from '../../api/saving.api'
import AllSavingsRecords from './components/AllSavingsRecords';
import { Card, Col, Empty, Row, Space } from 'antd';
import ReactEcharts from "echarts-for-react";
import { SimplePieChartOption } from '../../utils/SimplePieChartOption';
import useUserTheme from '../../hooks/useUserTheme';

function Saving() {
    const { user } = useSelector(state => state.user)
    const theme = useUserTheme()
    const [allSavings, setAllSavings] = useState([])
    const [allCategories, setAllCategories] = useState([])
    const [allSavingTotalByCategories, setAllSavingTotalByCategories] = useState([])

    const getAllSavings = async (userId) => {
        await getSavingByUserID(userId).then(res => {
            if (res && res.status !== false) {
                setAllSavings(res)
            }
        })
    }

    const getAllCategories = async (userId) => {
        await getExpenseCategories(userId).then((res) => {
          if (res && res.status !== false) {
            setAllCategories(res);
          }
        });
    }

    const getAllSavingTotalByCategories = async (userId) => {
        await getSavingTotalByCategories(userId).then(res => {
            if (res && res.status !== false) {
                setAllSavingTotalByCategories(res)
            }
        })
    }

    const getAllData = () => {
        const userId = user.id
        getAllSavings(userId)
        getAllCategories(userId)
        getAllSavingTotalByCategories(userId)
    }

    const prepareDataForPieChart = (data) => {
        return data.map(item => ({
            name: item.category,
            value: item.savingTotal
        }));
    };


    useEffect(() => {
        getAllData()
    }, [])

    return (
        <>
            <Space
                direction="vertical"
                size="small"
                style={{
                    display: 'flex',
                }}
            >
                <AllSavingsRecords allSavings={allSavings} getAllData={getAllData} allCategories={allCategories} />

                <Row>
                    <Col span={24}>
                        <Card style={{ width: "100%", padding: '20px 10%', borderRadius: 10, }}>
                            {allSavingTotalByCategories ? allSavingTotalByCategories && Object.keys(allSavingTotalByCategories) !== 0 && <ReactEcharts option={SimplePieChartOption("Saving Total By Categories", prepareDataForPieChart(allSavingTotalByCategories))} theme={theme} />
                                : <Empty description={"Don't have the saving total by categories"} />}
                        </Card>
                    </Col>
                </Row>
            </Space>
        </ >
    )
}

export default Saving