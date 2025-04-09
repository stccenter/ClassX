import React, { useEffect, useState, useRef } from 'react'
import { Slider, Table, Button, Space } from 'antd';
import { CloseOutlined, CheckOutlined } from "@ant-design/icons";
import { Link, useOutletContext } from 'react-router-dom'
import axios from 'axios'
import { ViewShareButton, ViewViewButton, ViewDownloadButton } from '../../component';

export default function Dataset() {
    const [data, setData] = useState([]);
    // const filterData = (data) => data.map(item=>item )
    const columns = [
        {
            title: 'File Name',
            dataIndex: 'fileName',
            key: 'fileName',
        },
        {
            title: 'Created By',
            dataIndex: 'createdBy',
            key: 'createdBy',
        },
        {
            title: 'Date Modified (EST)',
            dataIndex: 'dateModified',
            key: 'dateModified',
        },
        {
            title: 'Share By',
            dataIndex: 'shareBy',
            key: 'shareBy',
            render: (text, record, index) => {
                if (record.sharedBy) {
                    return (<CheckOutlined style={{ color: "green" }} />)
                }
                return (<CloseOutlined style={{ color: "red" }} />)
            }
        },
        {
            title: 'Action',
            dataIndex: 'action',
            key: 'action',
            render: (_, record) => {
                console.log("action record: ", record)
                return (
                    <Space>
                        <ViewShareButton record={record} />
                        <Link to="/dashboard/viewimage" style={{ color: "blue" }} state={{ id: record.id }}>
                            <ViewViewButton />
                        </Link>
                        <ViewDownloadButton id={record.id} />
                    </Space>
                )
            }
        },
    ];


    useEffect(() => {
        axios({
            // Endpoint to send files
            url: "/api/viewTrainingFiles/",
            method: "GET",
            headers: {},
        })
            // Handle the response from backend here
            .then((res) => {
                console.log(res)
                let tempData = res.data.map(item => {
                    return { key: item[0].id, id: item[0].id, fileName: item[0].file_name, createdBy: item[2], dateModified: item[1], sharedBy: item[0].shared_by == null ? false : true, }
                })
                console.log("tempData: ", tempData);
                setData(tempData)
            })
            // Catch errors if any
            .catch((err) => { console.log(err) });
    }, [])

    return (
        <Table style={{ height: "92vh" }} columns={columns} dataSource={data} />
    )
}
