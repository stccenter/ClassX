import React, { useRef, useEffect } from 'react'
import Piechart from "./Piechart"

export default function ImagePage({ data, labelImage, labelMap }) {
    console.log("data:", data)
    console.log("labelImage:", labelImage)

    useEffect(() => {

    }, [])
    return (
        <>
            <img style={{ width: 400 }} src={`${import.meta.env.VITE_SRC_URL}/${data.visualization_path}`} alt="" />
            <img style={{ width: 400 }} src={`${import.meta.env.VITE_SRC_URL}/${labelImage.color_image_path}`} alt="" />
	    {/* <img style={{ width: 400 }} src={`http://localhost:5000/static/${data.visualization_path}`} alt="" />
            <img style={{ width: 400 }} src={`http://localhost:5000/static/${labelImage.color_image_path}`} alt="" /> */}
            <Piechart segment_id={labelImage.segment_image_id} labelMap={labelMap} />
        </>
    )
}
