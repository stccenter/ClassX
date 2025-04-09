import React, { useEffect, useState } from 'react'
import { useOutletContext, useLocation, Navigate } from "react-router-dom";
import axios from 'axios'
import { Table } from "../../component"
import { UploadStructure } from "../../component"
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb';

// Define the type for the data passed via location state
interface ResearchFieldData {
    name: string;
    // Add other properties as required based on the actual data
}

interface Breadcrumb {
    name: string;
    url: string;
}

export default function Image(): JSX.Element {
    /*Page
        Image list for resesrch field.
        It includes 
            - image table which have a filter on top side and 
              list all image related information.
            - image upload button
    */

    // Get data from the previous page using useLocation
    const dataFromDomainCard = useLocation();
    const data = dataFromDomainCard.state.data;
    const { name } = data;

    // Get and set breadcrumb using useOutletContext
    const [breadcrumb, setBreadcrumb] = useOutletContext<[Breadcrumb[], React.Dispatch<React.SetStateAction<Breadcrumb[]>>]>();

    // State for fresh table reload
    const [uploadFresh, setUploadFresh] = useState(true)

    // Function to refresh the table
    const freshTable = () => {
        let temp = uploadFresh
        setUploadFresh(!temp)
    }

    // Effect to update breadcrumb when the component loads or uploadFresh changes
    useEffect(() => {
        // Set up breadcrumb with current name
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Research Field", url: "/dashboard/" }, { name: name, url: "/dashboard/images" }]))

    }, [uploadFresh])

    // If data is not available, redirect to dashboard
    if (!data) return <Navigate to="/dashboard" />

    return (
        <div style={{ height: "92vh" }}>
            <Table researchFieldData={data} />
            <UploadStructure researchFieldData={data} freshTable={freshTable} />
        </div>
        // <Test />
    )
}
