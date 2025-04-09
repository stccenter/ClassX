import { useState, useEffect } from 'react'
import { useOutletContext } from "react-router-dom";
import axios from "axios"
import styled from "@emotion/styled"
import DomainGallery from '../../component/dashboard/researchField/DomainGallery'
import { DomainCard, DomainCardContainer } from '../../component'
import img1 from "../../assets/home_img1.png" // Heliophysics
import img2 from "../../assets/home_img2.png"
import useConvertToBreadcrumb from '../../hooks/useConvertToBreadcrumb'

export default function Domain(props) {
    console.log("props on domain:", props)

    // TODO: when add new research field, need to fetch data again 
    const [fieldList, setFieldList] = useState([])
    const [breadcrumb, setBreadcrumb] = useOutletContext()
    useEffect(() => {
        console.log("hello")
        // set up breadcrumb
        setBreadcrumb(useConvertToBreadcrumb([{ name: "Research Field" }]))
        let ignore = false;
        // console.log(`${import.meta.env.VITE_API_URL}getDefaultResearchFields`)
        axios({
            // Endpoint to send files
            url: `/api/getDefaultResearchFields`,
            method: "GET",
            headers: {},
        })
            // Handle the response from backend here
            .then((res) => {
                // console.log(`${import.meta.env.VITE_API_URL}getDefaultResearchFields`, res)
                if (!ignore) {
                    setFieldList(res.data.research_fields
                        .filter(item => item.id !== 1)
                        .map(item => {
                            item.src = img1;
                            return item;
                        }))
                    console.log(fieldList)
                }
            })

            // Catch errors if any
            .catch((err) => { console.log(err) });
        return () => {
            ignore = true;
        }
    }, [])

    return (
        <Container>
            <DomainGallery title="Research Field" Card={DomainCard} data={fieldList} CardContainer={DomainCardContainer} />
        </Container>
    )
}

const Container = styled.div`
    height: 92vh;
    width: 100%;
`