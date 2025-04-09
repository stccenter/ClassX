import React, { useState } from 'react';
import { Button, Form, Input, Radio, Switch, Slider, Tooltip } from 'antd';
import styled from "@emotion/styled"
import SlideInput from './SlideInput';

export default function SegmentForm(props) {
    const { previewData, cropImageID } = props;
    const [_form] = Form.useForm();
    const [algorithmSelect, setAlgorithmSelect] = useState('algorithm_SLIC');
    const [colorClustering, setColorClustering] = useState(false)
    const [smallFeatureRemoval, setSmallFeatureRemoval] = useState(false)
    const [regionMerging, setRegionMerging] = useState(false)
    // algorithm value
    const [segmentationLevel, setSegmentationLevel] = useState(12)
    const [compacting, setCompacting] = useState(5)
    const [SLIC_gaussSigma, setSLIC_gaussSigma] = useState(0.5)
    const [qs_gaussSigma, setQs_gaussSigma] = useState(1.2)
    const [kernalSize, setKernalSize] = useState(3)
    const [maxDistance, setMaxDistance] = useState(10)
    const [ws_gaussSigma, setWs_gaussSigma] = useState(7)
    const [featureSeparation, setFeatureSeparation] = useState(10)
    const [fs_gaussSigma, setFs_gaussSigma] = useState(0.8)
    const [scale, setScale] = useState(1)
    const [minimumSize, setMinimumSize] = useState(20)
    const formItemStyle = { marginBottom: "0.5rem" };


    const onFormLayoutChange = ({ layout }) => {
        if (/^algorithm_.+$/.test(layout)) {
            setAlgorithmSelect(layout);
        }
    };

    const setValue = (value) => {
        console.log("setValue:", value)
        return value;
    }
    const onFinish = (values) => {
        console.log("values:", values)
        const form = [];

        //TODO: faker data for test 
        form.push({ name: "id", value: cropImageID });
        form.push({ name: "name", value: "123" });
        form.push({ name: "confirm", value: 1 });

        // Multi-processing
        form.push({ name: "multiProcessingCheck", value: 0 });
        if (values.multProcessing) {
            form.push({ name: "multiProcessingCheck", value: 1 });
        }
        // Light Adjustment
        form.push({ name: "LightAdjustmentCheck", value: 0 });
        if (values.lightAdjustment) {
            form.push({ name: "LightAdjustmentCheck", value: 1 });
        }
        // Light Adjustment
        form.push({ name: "ContrastStretchCheck", value: 0 });
        if (values.contrastStretching) {
            form.push({ name: "ContrastStretchCheck", value: 1 });
        }
        // Color Cluster
        form.push({ name: "ColorClustCheck", value: 0 });
        form.push({ name: "menuColor", value: values.colorClusteringItem == "adaptive" ? 1 : 2 });
        form.push({ name: "Color_Clusters0", value: values.colorClusteringValue === undefined ? 0 : values.colorClusteringValue });
        if (values.colorClustering) {
            form.push({ name: "ColorClustCheck", value: 1 });
        }
        // Algorithm Setting
        let param1, param2, param3;
        if (values.layout == "algorithm_watershed") {
            param1 = featureSeparation;
            param2 = 0;
            param3 = ws_gaussSigma;
            form.push({ name: "menu", value: 1 });
        } else if (values.layout == "algorithm_SLIC") {
            param1 = segmentationLevel;
            param2 = compacting;
            param3 = SLIC_gaussSigma;
            form.push({ name: "menu", value: 2 });
        } else if (values.layout == "algorithm_quickshift") {
            param1 = kernalSize;
            param2 = maxDistance;
            param3 = qs_gaussSigma;
            form.push({ name: "menu", value: 3 });
        } else if (values.layout == "algorithm_maskrcnn") {
            param1 = 0;
            param2 = 0;
            param3 = 0;
            form.push({ name: "menu", value: 5 });

        }
         else {
            param1 = scale;
            param2 = minimumSize;
            param3 = fs_gaussSigma;
            form.push({ name: "menu", value: 4 });
        }
        form.push({ name: "param1", value: param1 });
        form.push({ name: "param2", value: param2 });
        form.push({ name: "param3", value: param3 });
        // Small Feature Removal
        form.push({ name: "small_rem", value: 0 });
        form.push({ name: "rem_threshold", value: values.smallFeatureRemovalValue === undefined ? 0 : values.smallFeatureRemovalValue });
        if (values.smallFeatureRemoval) {
            form.push({ name: "small_rem", value: 1 });

        }
        // Region Merging
        form.push({ name: "RAGCheck", value: 0 });
        form.push({ name: "menuRAG", value: values.regionMergingItem == 'thresholdCut' ? 1 : values.regionMergingItem == 'normalizedCut' ? 2 : 3 });
        form.push({ name: "RAG_Threshold0", value: values.regionMergingValue === undefined ? 0 : values.regionMergingValue });
        if (values.regionMerging) {
            form.push({ name: "RAGCheck", value: 1 });
        }
        console.log("Final Form: ", form)
        previewData(form, values.lightAdjustment);
    }
    return (
        <Form
            labelCol={{ span: 10 }}
            wrapperCol={{ span: 14 }}
            layout={algorithmSelect}
            form={_form}
            initialValues={{
                layout: algorithmSelect,
            }}
            onValuesChange={onFormLayoutChange}
            onFinish={onFinish}
            style={{
                maxWidth: algorithmSelect === 'inline' ? 'none' : 900,
                padding: "0.5rem"
            }}
            size='middle'
        >
            <h2>Pre-Processing</h2>
            {/* preprocess selector */}
            <Tooltip title="Image Manipulation and Adjustments to prepare it for segmentation.">
                <Form.Item style={formItemStyle} label="Multi Processing" name="multProcessing" valuePropName="checked" initialValue={false} >
                    <Switch />
                </Form.Item>
            </Tooltip>

            <Tooltip title="Generates additional image previews for the user to pick. The images have their lighting adjusted before segmentation.">
                <Form.Item style={formItemStyle} label="Light Adjustment" name="lightAdjustment" valuePropName="checked" initialValue={false} >
                    <Switch />
                </Form.Item>
            </Tooltip>

            <Tooltip title="Increases the distance between the lowest and highest intensity pixels and levels out the rest between that range.">
                <Form.Item style={formItemStyle} label="Contrast Stretching" name="contrastStretching" valuePropName="checked" initialValue={false} >
                    <Switch />
                </Form.Item>
            </Tooltip>

            <Tooltip title="Determines most dominant colors based on number of clusters using an Adaptive or KMeans algorithm and quantizes the image to a reduced palette of those dominant colors.">
                <Form.Item style={formItemStyle} label="Color Clustering" >
                    <Form.Item style={formItemStyle} name="colorClustering" valuePropName="checked" initialValue={false} >
                        <Switch onChange={(checked) => { setColorClustering(checked) }} />
                    </Form.Item>
                    <Form.Item style={formItemStyle} name="colorClusteringItem"
                        layout='vertical'
                        rules={colorClustering ? [
                            {
                                required: true,
                                message: 'Please select Color Clustering Method!',
                            },
                        ] : null}>
                        <Radio.Group disabled={!colorClustering}>
                            <Radio.Button value="adaptive">adaptive</Radio.Button>
                            <Radio.Button value="k_means">K-means</Radio.Button>
                        </Radio.Group>
                    </Form.Item>
                    <Form.Item style={formItemStyle} name="colorClusteringValue"
                        layout='vertical'
                        rules={colorClustering ? [
                            {
                                required: true,
                                message: 'Please select Color Clustering value!',
                            },
                        ] : null}>
                        <Slider min={1} max={25} disabled={!colorClustering} />
                    </Form.Item>
                </Form.Item>
            </Tooltip>

            {/* algorithm selector */}
            <Form.Item style={formItemStyle} label="Algorithm Selector" name="layout">
                <Radio.Group value={algorithmSelect} buttonStyle='solid' >
                    <Radio.Button value="algorithm_SLIC">SLIC</Radio.Button>
                    <Radio.Button value="algorithm_quickshift">Quickshift</Radio.Button>
                    <Radio.Button value="algorithm_watershed">Watershed</Radio.Button>
                    <Radio.Button value="algorithm_Felzenswalb">Felzenswalb</Radio.Button>
                    <Radio.Button value="algorithm_maskrcnn">Mask-RCNN</Radio.Button>
                </Radio.Group>
            </Form.Item>

            {/* algorithm switch area */}
            <Algorithm style={{ display: `${algorithmSelect == "algorithm_SLIC" ? "block" : "none"}` }}>
                <h2>SLIC Segmentation</h2>
                <Form.Item style={formItemStyle} label="Segmentation Level" name="segmentationLevel" getValueFromEvent={setValue}>
                    <SlideInput min={1} max={25} step={1} defaultValue={segmentationLevel} setValue={setSegmentationLevel} />
                </Form.Item>
                <Form.Item style={formItemStyle} label="Compacting" name="compacting" >
                    <SlideInput min={1} max={50} step={1} defaultValue={compacting} setValue={setCompacting} />
                </Form.Item>
                <Form.Item style={formItemStyle} label="Gauss Sigma" name="SLIC_gaussSigma" >
                    <SlideInput min={0} max={10} step={0.1} defaultValue={SLIC_gaussSigma} setValue={setSLIC_gaussSigma} />
                </Form.Item>
            </Algorithm>
            <Algorithm style={{ display: `${algorithmSelect == "algorithm_quickshift" ? "block" : "none"}` }}>
                <h2>Quickshift Segmentation</h2>
                <Form.Item style={formItemStyle} label="Gauss Sigma" name="qs_gaussSigma" >
                    <SlideInput min={0} max={10} step={0.1} defaultValue={qs_gaussSigma} setValue={setQs_gaussSigma} />
                </Form.Item>
                <Form.Item style={formItemStyle} label="Kernal Size" name="kernalSize" >
                    <SlideInput min={1} max={20} step={1} defaultValue={kernalSize} setValue={setKernalSize} />
                </Form.Item>
                <Form.Item style={formItemStyle} label="Max Distance" name="maxDistance" >
                    <SlideInput min={1} max={50} step={1} defaultValue={maxDistance} setValue={setMaxDistance} />
                </Form.Item>
            </Algorithm>

            <Algorithm style={{ display: `${algorithmSelect == "algorithm_watershed" ? "block" : "none"}` }}>
                <h2>Watershed Segmentation</h2>
                <Form.Item style={formItemStyle} label="Gauss Sigma" name="ws_gaussSigma" >
                    <SlideInput min={0} max={10} step={0.1} defaultValue={ws_gaussSigma} setValue={setWs_gaussSigma} />
                </Form.Item>
                <Form.Item style={formItemStyle} label="Feature Separation" name="featureSeparation" >
                    <SlideInput min={1} max={30} step={1} defaultValue={featureSeparation} setValue={setFeatureSeparation} />
                </Form.Item>
            </Algorithm>
            <Algorithm style={{ display: `${algorithmSelect == "algorithm_Felzenswalb" ? "block" : "none"}` }}>
                <h2>Felzenswalb Segmentation</h2>
                <Form.Item style={formItemStyle} label="Gauss Sigma" name="fs_gaussSigma" >
                    <SlideInput min={0} max={10} step={0.1} defaultValue={fs_gaussSigma} setValue={setFs_gaussSigma} />
                </Form.Item>
                <Form.Item style={formItemStyle} label="Scale" name="scale" >
                    <SlideInput min={1} max={20} step={1} defaultValue={scale} setValue={setScale} />
                </Form.Item>
                <Form.Item style={formItemStyle} label="Minimum Size" name="minimumSize" >
                    <SlideInput min={1} max={30} step={1} defaultValue={minimumSize} setValue={setMinimumSize} />
                </Form.Item>
            </Algorithm>
            <Algorithm style={{ display: `${algorithmSelect == "algorithm_maskrcnn" ? "block" : "none"}` }}>
                <h2>Mask-RCNN</h2>
            </Algorithm>

            {/* postprocesser selector */}
            <h2>Post-Processing</h2>
            {/* preprocess selector */}
            <Form.Item style={formItemStyle} label="Small Feature Removal">
                <Form.Item style={formItemStyle} name="smallFeatureRemoval" valuePropName="checked" initialValue={false} >
                    <Switch onChange={(checked) => { setSmallFeatureRemoval(checked) }} />
                </Form.Item>
                <Form.Item name="smallFeatureRemovalValue"
                    rules={smallFeatureRemoval ? [
                        {
                            required: true,
                            message: 'Please select Small Feature Removal value!',
                        },
                    ] : null}
                >
                    <Slider min={1} max={50} defaultValue={25} disabled={!smallFeatureRemoval} />
                </Form.Item>
            </Form.Item>
            <Form.Item style={formItemStyle} label="Region Merging">
                <Form.Item style={formItemStyle} name="regionMerging" valuePropName="checked" initialValue={false} >
                    <Switch onChange={(checked) => { setRegionMerging(checked) }} />
                </Form.Item>
                <Form.Item style={formItemStyle} name="regionMergingItem"
                    rules={regionMerging ? [
                        {
                            required: true,
                            message: 'Please select Region Merging Method!',
                        },
                    ] : null} >
                    <Radio.Group disabled={!regionMerging}>
                        <Radio.Button value="thresholdCut">Threshold Cut</Radio.Button>
                        <Radio.Button value="normalizedCut">Normalized Cut</Radio.Button>
                        <Radio.Button value="mergeHierachical">Merge Hierachical</Radio.Button>
                    </Radio.Group>
                </Form.Item>
                <Form.Item style={formItemStyle} name="regionMergingValue"
                    rules={regionMerging ? [
                        {
                            required: true,
                            message: 'Please select Region Merging value!',
                        },
                    ] : null}
                >
                    <Slider min={1} max={50} defaultValue={10} step={0.1} disabled={!regionMerging} />
                </Form.Item>
            </Form.Item>
            {/* submit result */}
            <Form.Item style={formItemStyle}>
                <Button type="primary" htmlType="submit">Submit</Button>
            </Form.Item >
        </Form >

    )
}

const Algorithm = styled.div`
    
`
