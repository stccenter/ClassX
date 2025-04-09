import React, { useEffect } from 'react'
import styled from "@emotion/styled"
import GalleryCard from './GalleryCard'

export default function GalleryContainer({ data, page, curPage, orgImageList, segImages, labelImages, labelMap }) {
    console.log("data:", data)
    console.log("orgImageList: ", orgImageList)

    return (
        <Container css={{ display: `${page === curPage ? 'flex' : "none"}` }}>
            {
                data.map(item => {
                    console.log("item.original_image_id:", item.original_image_id)
                    console.log("data.original_image_id:", data.original_image_id)
                    return (
                        <GalleryCard source={item} key={item.id}
                            orgImage={orgImageList.filter(image => {
                                return image.id == item.original_image_id;
                            })}
                            segImage={segImages.filter(image => {
                                return image.crop_image_id == item.id;
                            })}
                            labelImages={labelImages}
                            labelMap={labelMap} />
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

