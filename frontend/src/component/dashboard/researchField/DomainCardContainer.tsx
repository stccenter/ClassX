import React, { useState } from 'react'
import styled from "@emotion/styled"

export default function DomainCardContainer({ data, page, curPage, Card }) {

    return (
        <Container style={{ display: `${page === curPage ? 'flex' : "none"}` }}>
            {
                data.map(item => {
                    return (
                        <Card data={item} key={item.id} />
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

