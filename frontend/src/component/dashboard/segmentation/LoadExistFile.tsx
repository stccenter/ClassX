import React, { useEffect, useState } from 'react'
import { Input, Radio, Space } from 'antd';
import axios from 'axios'
export default function LoadExistFile(props) {

    const { getTrainingFileName, research_id } = props
    const [trainingFiles, setTrainingFiles] = useState()

    const onChange = (e) => {
        console.log('radio checked', e.target.value);
        getTrainingFileName(e.target.value)
    }
    useEffect(() => {
        axios({
            url: "/api/getTrainingFiles/",
            method: "GET",
            headers: {},
            params: {
                name: "123",
                research_id: research_id
            }
        }).then((res) => {
            console.log("training_files:", res.data.training_files)
            let tempTrainingFile = res.data.training_files.map(item => {
                return (<Radio key={item.id} value={item.file_name}>{item.file_name}</Radio>)
            })
            setTrainingFiles(tempTrainingFile)
        }).catch((err) => { console.log(err) });
    }, [])
    return (
        <Radio.Group onChange={onChange}>
            <Space direction="vertical">
                {trainingFiles}
            </Space>
        </Radio.Group>
    )
}
