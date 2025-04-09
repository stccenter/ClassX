import React from 'react'
import styled from "@emotion/styled"
import SegmentGalleryCard from './SegmentGalleryCard'

export default function SegmentGalleryContainer({ data, page, curPage }) {
    // console.log("data:", data)
    // console.log("container curpage: ", curPage)
    return (
        <Container style={{ display: `${page === curPage ? 'flex' : "none"}` }}>
            {
                data.map(item => {
                    return (
                        <SegmentGalleryCard source={item} key={item.id} />
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

