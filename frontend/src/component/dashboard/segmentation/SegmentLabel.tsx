import React, { useState, useEffect, useRef } from 'react'
import axios from "axios"
import { Radio, Form, Tabs, Button, Select, Slider, Statistic, Switch, Modal } from 'antd';
import styled from "@emotion/styled"
import { Barchart, Piechart } from "../.."
import SegmentLabelForm from './SegmentLabelForm';
import SegmentLabelSave from './SegmentLabelSave'

export default function SegmentLabel(props) {
    // console.log("SegmentLabel props:", props)

    const canvasRef = useRef(null);
    const { id, crop_image_id, marked_image_path, research_id } = props.data;
    const [labelMap, setLabelMap] = useState(null)
    const [curLabel, setCurLabel] = useState(1)
    const [labeledSegmentsNum, setLabeledSegmentsNum] = useState(0)
    const [totalSegmentsNum, setTotalSegmentsNum] = useState(0)
    const [barchartData, setBarchartData] = useState([])
    const [barchartLabel, setBarchartLabel] = useState([])
    const [barchartColor, setBarchartColor] = useState([])
    const [pieData, setPieData] = useState([])
    const [pieLabelClassList, setPieLabelClassList] = useState(null)
    // const [chartSwitch, setChartSwitch] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [trainingFileComponent, setTrainingFileComponent] = useState(null)
    // save training file
    const [opacityValue, setOpacityValue] = useState(0.5)
    const [smallAreaMerge, setSmallAreaMerge] = useState(false)
    const [smallAreaMergeValue, setSmallAreaMergeValue] = useState(0)
    const [saveType, setSaveType] = useState(1)
    const [trainingFileName, setTrainingFileName] = useState("")
    const [probThreshold, setProbThreshold] = useState(0)
    const [ALAlgorithm, setALAlgorithm] = useState(1)
    const [trainingFileId, setTrainingFileId] = useState(0)


    // Auto label -- update Probability Threshold 
    const updateProbThreshold = (value) => {
        setProbThreshold(value)
    }
    // Auto label
    const autoLabel = () => {
        console.log("prob_threshold", probThreshold)
        console.log("algorithm_id", ALAlgorithm)
        console.log("training_file_id", trainingFileId)
        axios({
            url: "/api/autoLabelImage/",
            method: "GET",
            headers: {},
            params: {
                segment_image_id: id,
                prob_threshold: probThreshold,
                algorithm_id: ALAlgorithm,
                training_file_id: trainingFileId
            }
        }).then((res) => {
            console.log("/api/autoLabelImage/:", res)
            loadSegmentImage()
        }).catch((err) => { console.log(err) });
    }

    // Save training model -- set small area value
    const updateSmallAreaValue = (value) => {
        setSmallAreaMergeValue(value)
    }

    // Save training model -- update training file name
    const updateTrainingFileName = (name) => {
        setTrainingFileName(name)
    }

    // Save training model -- update save type either create a new model or save to exist type
    const updateSaveType = (saveType) => {
        setSaveType(saveType)
    }

    const showModal = () => {
        setIsModalOpen(true);
    };

    // Save training model -- save model to backend
    const handleOk = () => {
        // console.log("segment_image_id:", id);
        // console.log("opacity_value:", opacityValue);
        // console.log("file_type:", "HDF5");
        // console.log("save_type:", saveType);
        // console.log("training_file_name:", trainingFileName);
        // console.log("remove_small_labels:", smallAreaMerge);
        // console.log("area_removal_percentage:", smallAreaMergeValue);

        // check if all segments are labeled
        if (totalSegmentsNum != labeledSegmentsNum) {
            if (confirm("Not all segments are labeled. Unlabeled segments are assigned to 'Unknown' class. Please click OK to confirm.")) {
                axios({
                    url: "/api/setUnlabeledUnknown/",
                    method: "GET",
                    headers: {},
                    params: {
                        segment_image_id: id,
                        remove_small_labels: smallAreaMerge,
                        area_removal_percentage: smallAreaMergeValue,
                    }
                }).then((res) => {
                    console.log("unlabel part will be unknow:", res)
                    // loadSegmentImage()
                    axios({
                        url: "/api/saveTrainingFile/",
                        method: "GET",
                        headers: {},
                        params: {
                            segment_image_id: id,
                            opacity_value: opacityValue,
                            file_type: "HDF5",
                            save_type: saveType,
                            training_file_name: trainingFileName,
                            remove_small_labels: smallAreaMerge,
                            area_removal_percentage: smallAreaMergeValue,
                        }
                    }).then((res) => {
                        console.log("save current label:", res)
                        loadSegmentImage()

                    }).catch((err) => { console.log(err) });
                    setIsModalOpen(false);

                }).catch((err) => { console.log(err) });
                setIsModalOpen(false);
            }
        } else {
            axios({
                url: "/api/saveTrainingFile/",
                method: "GET",
                headers: {},
                params: {
                    segment_image_id: id,
                    opacity_value: opacityValue,
                    file_type: "HDF5",
                    save_type: saveType,
                    training_file_name: trainingFileName,
                    remove_small_labels: smallAreaMerge,
                    area_removal_percentage: smallAreaMergeValue,
                }
            }).then((res) => {
                console.log("save current label:", res)
                loadSegmentImage()

            }).catch((err) => { console.log(err) });
            setIsModalOpen(false);
        }
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };
    const onChange = (e) => {
        setCurLabel(e.target.value)
    };

    // Save training model -- update opacity
    const updateOpacity = (value) => {
        setOpacityValue(value);
        const canvas = canvasRef.current;
        let ctx = canvas.getContext("2d");
        axios({
            url: "/api/updateLabelOpacity/",
            method: "GET",
            headers: {},
            params: {
                segment_image_id: id,
                opacity_value: value
            }
        }).then((res) => {
            var segObj = new Image();
            segObj.onload = function () {
                ctx.drawImage(this, 0, 0, this.width, this.height, 0, 0, canvas.width, canvas.height);
            }
            segObj.src = 'data:image/png;base64,' + res.data.image_string;

        }).catch((err) => { console.log(err) });
    }

    // Chart -- switch bar chart and pie chart
    // const updateChartSwitch = (checked) => {
    //     console.log("updateChartSwitch:", checked);
    //     setChartSwitch(checked)
    // }

    // Canvas -- Get mouse position
    const getMousePos = (canvas, evt) => {
        let canvasCoords = canvas.getBoundingClientRect();
        return {
            x: evt.clientX - parseInt(canvasCoords.left),
            y: evt.clientY - parseInt(canvasCoords.top)
        };
    }

    // Chart -- set up bar chart and pie chart
    const setChart = (labeledData) => {
        let tempBarchartData = barchartData;
        let tempPiechartData = pieData;
        // console.log("tempBarchartData:", tempBarchartData)
        // console.log("tempPiechartData:", tempPiechartData)
        // console.log("labelMap:", labelMap)
        labeledData.forEach(item => {
            if (item[0] != 0) {
                tempBarchartData[item[0] - 1] = item[1]
                // tempPiechartData[item[0] - 1].value = item[1]
            }
        })
        for (let i = 0; i < tempBarchartData.length; i++) {
            if (tempBarchartData[i] == undefined) {
                tempBarchartData[i] = 0;
            }
        }
        setBarchartData(tempBarchartData)
        setPieLabelClassList(labeledData)
    }

    const updateLabelImage = (ctx, image_string) => {
        let segObj = new Image();
        segObj.onload = function () {
            let ratio = this.height / this.width
            ctx.canvas.width = 4096;
            ctx.canvas.height = ctx.canvas.width * ratio;
            ctx.drawImage(this, 0, 0, ctx.canvas.width, ctx.canvas.height);
        }
        segObj.src = 'data:image/png;base64,' + image_string;
    }

    // mouse click action to label segment image 
    const segmentImageClick = (evt) => {
        // get canvas of original image 
        const canvas = canvasRef.current;
        let ctx = canvas.getContext("2d");
        // get mouse position on canvas of original image
        let mousePos = getMousePos(canvas, evt);
        let x = parseInt(mousePos.x);
        let y = parseInt(mousePos.y);
        let actualSize = canvas.offsetWidth;
        axios({
            url: "/api/labelSegment/",
            method: "GET",
            headers: {},
            params: {
                segment_image_id: id,
                x: x,
                y: y,
                actualSize: actualSize,
                label_id: curLabel
            }
        }).then((res) => {
            // update label image
            updateLabelImage(ctx, res.data.image_string)
            // update labeled segments counter
            setTotalSegmentsNum(res.data.total_segments)
            setLabeledSegmentsNum(res.data.labeled_segments)
            // update statistics chart
            setChart(res.data.label_class_list)

        }).catch((err) => { console.log(err) });
    }

    // const setOpacity = (value) => {
    //     console.log("setOpacity value: ", value)
    // }

    const loadSegmentImage = () => {
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');
        let image = new Image(); // Using optional size for image
        image.src = `${import.meta.env.VITE_SRC_URL}/${marked_image_path}`;
        // image.src = `http://localhost:5000/static/${marked_image_path}`;
        image.onload = drawImageActualSize;
        function drawImageActualSize() {
            // imagedata = this;
            canvas.width = 512;
            canvas.height = 512;
            context.drawImage(this, 0, 0, this.width, this.height, 0, 0, canvas.width, canvas.height);
        }
        axios({
            url: "/api/dashboard/label",
            method: "GET",
            headers: {},
            params: { crop_image_id: crop_image_id }
        }).then((res) => {
            console.log("/api/dashboard/label res:", res)
            // set autolabel select <Select.Option value="HDF5">HDF5</Select.Option>
            let tempTrainingFileComponent = res.data.training_files.map(item => {
                return (<Select.Option key={item.id} value={item.id}>{item.file_name}</Select.Option>)
            })
            setTrainingFileComponent(tempTrainingFileComponent)
            //set up label map select bar 
            let tempLabelMap = null;
            let tempBarchartColor = [];
            let tempBarchartLabel = [];
            let tempPiechart = []
            tempLabelMap = res.data.label_map.map(item => {
                tempBarchartLabel.push(item.name);
                tempBarchartColor.push(item.color);
                tempPiechart.push({ id: item.id, value: 0, label: item.name, color: item.color })
                return (<Radio.Button style={{ background: item.color, color: item.textcolor }} value={item.id} key={item.id}>{item.name}</Radio.Button>)
            })
            setBarchartData(new Array(tempBarchartLabel.length))
            setBarchartColor(tempBarchartColor)
            setPieData(tempPiechart)
            setBarchartLabel(tempBarchartLabel)
            setLabelMap(tempLabelMap)
        }).catch((err) => { console.log(err) });

        axios({
            url: "/api/getLabelImage/",
            method: "GET",
            headers: { 'Content-Type': 'application/json', },
            params: { segment_image_id: id }
        }).then((res) => {
            // initialize label image
            updateLabelImage(context, res.data.image_string)
            // set labeled segments counter
            setTotalSegmentsNum(res.data.total_segments)
            setLabeledSegmentsNum(res.data.labeled_segments)
            // set statistic chart
            setChart(res.data.label_class_list)

        }).catch((err) => { console.log(err) });
        axios({
            url: "/api/getLabelArea/",
            method: "GET",
            headers: {},
            params: { segment_image_id: id }
        }).then((res) => {
            // console.log("/api/getLabelArea res:", res)

        }).catch((err) => { console.log(err) });
    }

    useEffect(() => {
        loadSegmentImage()
    }, [])
    return (
        <div style={{ display: "flex" }}>
            <div style={{ textAlign: "center", marginRight: "1rem" }}>
                <div>
                    <Radio.Group onChange={onChange} buttonStyle="solid">
                        {
                            labelMap
                        }
                    </Radio.Group>
                </div>
                <canvas style={{ width: 500, marginTop: "1rem", marginBottom: "1rem" }} ref={canvasRef} onClick={segmentImageClick} />
                <Statistic title="Labeled Segments" value={labeledSegmentsNum} suffix={`/ ${totalSegmentsNum}`} />

            </div>
            <div >
                <div style={{ height: 300, width: 600 }}>

                    <Tabs
                        defaultActiveKey="1"
                        tabPosition="top"
                        style={{
                            height: 220,
                        }}
                        items={[
                            {
                                key: '1',
                                label: 'Barchart',
                                children: (<Barchart data={barchartData} label={barchartLabel} color={barchartColor} />),
                            },
                            {
                                key: '2',
                                label: 'Piechart',
                                children: (<Piechart data={pieData} labelClass={pieLabelClassList} />),
                            }
                        ]}
                    />
                </div>
                <Tabs
                    defaultActiveKey="1"
                    tabPosition="top"
                    style={{
                        height: 220,
                    }}
                    items={[
                        {
                            key: '1',
                            label: 'Save training model',
                            children: (<Form
                                labelCol={{ span: 14 }}
                                wrapperCol={{ span: 20 }}
                                layout="horizontal"
                                style={{ maxWidth: 1000 }}
                            >
                                <Form.Item label="Opacity">
                                    <Slider min={0} max={1} step={0.1} defaultValue={0.6} onChange={updateOpacity} />
                                </Form.Item>
                                <Form.Item label="Select Type" >
                                    <Select defaultValue="HDF5">
                                        <Select.Option value="HDF5">HDF5</Select.Option>
                                    </Select>
                                </Form.Item>
                                <Form.Item label="Small Area Merge" >
                                    <Form.Item name="smallAreaMerge" valuePropName="checked" initialValue={false} >
                                        <Switch onChange={(checked) => { setSmallAreaMerge(checked) }} />
                                    </Form.Item>
                                    <Form.Item name="smallAreaMergeValue"
                                        layout='vertical'
                                        rules={smallAreaMerge ? [
                                            {
                                                required: true,
                                                message: 'Please select Small Area Merge value!',
                                            },
                                        ] : null}>
                                        <Slider min={0} max={1} step={0.1} disabled={!smallAreaMerge} onChangeComplete={updateSmallAreaValue} />
                                    </Form.Item>
                                </Form.Item>
                                <Button type="primary" onClick={showModal}>
                                    Save
                                </Button>
                                <Modal title="Save Labeling" open={isModalOpen} onOk={handleOk} onCancel={handleCancel}>
                                    <SegmentLabelSave updateSaveType={updateSaveType} updateTrainingFileName={updateTrainingFileName} research_id={research_id} />
                                </Modal>

                            </Form>),
                        },
                        {
                            key: '2',
                            label: 'Auto Labeling',
                            children: (<Form
                                labelCol={{ span: 14 }}
                                wrapperCol={{ span: 20 }}
                                layout="horizontal"
                                style={{ maxWidth: 1000 }}
                            >
                                <Form.Item label="Probability Threshold">
                                    <Slider initialValue={0.5} min={0} max={1} step={0.1} onChangeComplete={updateProbThreshold} />
                                </Form.Item>
                                <Form.Item label="Model Selection:" >
                                    <Select defaultValue="1" onChange={setALAlgorithm}>
                                        <Select.Option value="1">Random Forest</Select.Option>
                                        <Select.Option value="0">SVM</Select.Option>
                                        <Select.Option value="2">XGBoost</Select.Option>
                                        <Select.Option value="3">KNN</Select.Option>
                                    </Select>
                                </Form.Item>
                                <Form.Item label="Training File Selection:">
                                    <Select onChange={setTrainingFileId}>
                                        {trainingFileComponent}
                                    </Select>
                                </Form.Item>
                                <Button onClick={autoLabel}>Auto Label</Button>

                            </Form>),
                        }
                    ]}
                />

            </div>

        </div>
    )
}


