import React from 'react'
import styled from "@emotion/styled"

export interface CropCardData {
    source: string;
    name: string;
    title: string
    id: string;
    originalImage: any;
    researchFieldData: any;
}

export interface CropCardContainerProps {
    data: CropCardData[];
    page: number;
    curPage: number;
    Card: any;
    originalImage: any;
    researchFieldData: any;
}

export default function CropCardContainer({ data, page, curPage, Card, originalImage, researchFieldData }: CropCardContainerProps) {
    // console.log("data:", data)
    // console.log("container curpage: ", curPage)
    return (
        <Container style={{ display: `${page === curPage ? 'flex' : "none"}` }}>
            {
                data.map(item => {
                    return (
                        <Card source={item} title={item.name} key={item.id} originalImage={originalImage} researchFieldData={researchFieldData} />
                    )
                })
            }
        </Container >
    )
}



const Container = styled.div`
    width: 100%;
    height:100%;
    flex-wrap: wrap;
`

