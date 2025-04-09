import React, { useEffect, useState } from 'react'
import { ViewGallery } from '../../component'
import { useOutletContext, useLocation } from "react-router-dom";
import axios from "axios"
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb';

export default function ViewImage() {

    const dataFromDataset = useLocation()
    const trainingSetID = dataFromDataset.state.id;
    const [breadcrumb, setBreadcrumb] = useOutletContext()
    const [cropData, setCropData] = useState([])
    const [orgData, setOrgData] = useState([])
    const [segData, setSegData] = useState([])
    const [labelData, setLabelData] = useState([])
    const [labelMap, setLabelMap] = useState([])
    useEffect(() => {
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Training Datasets", url: "/dashboard/dataset" }, { name: "View Dataset", url: "/dashboard/viewimage" }]))
        axios({
            // Endpoint to send files
            url: "/api/getTrainingFileContents/",
            method: "GET",
            params: { training_file_id: trainingSetID }
        }).then((res) => {
            console.log("res", res)
            setOrgData(res.data.original_images)
            setCropData(res.data.crop_images)
            setSegData(res.data.segment_images)
            setLabelData(res.data.label_images)
            setLabelMap(res.data.label_map)
        }).catch((err) => { console.log(err) });
    }, [])

    return (
        <div style={{ height: "92vh" }}>
            <ViewGallery title={"Image View"} cardNum={8} cropData={cropData} orgData={orgData} segData={segData} labelData={labelData} labelMap={labelMap} />
        </div>
    )
}
