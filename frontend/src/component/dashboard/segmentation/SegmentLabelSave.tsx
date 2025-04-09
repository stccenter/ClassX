import React, { useState } from 'react';
import { Radio, Tabs, Input, TabsProps } from 'antd';
import LoadExistFile from '../../../component/dashboard/segmentation/LoadExistFile';
const SegmentLabelSave = (props) => {


    const [saveType, setSaveType] = useState(1)
    const { updateSaveType, updateTrainingFileName, research_id } = props;
    const [mode, setMode] = useState<TabsProps['tabPosition']>('top');

    const getTrainingFileName = (e) => {
        if (saveType == 1) {
            console.log("getTrainingFileName:", e.target.value)
            updateTrainingFileName(e.target.value + '.h5')
        } else {
            updateTrainingFileName(e)
        }

    }

    const getSaveType = (key) => {
        console.log("save-type:", key)
        setSaveType(key)
        updateSaveType(key)
    }
    return (
        <div style={{ height: "40vh" }}>
            <Tabs
                defaultActiveKey="1"
                tabPosition={mode}
                onChange={getSaveType}
                style={{
                    height: 220,
                }}
                items={[
                    {
                        key: '1',
                        label: 'Create new training file',
                        children: (<Input placeholder="Please enter training file name" addonAfter=".h5" onChange={getTrainingFileName} />),
                    },
                    {
                        key: '2',
                        label: 'Save to exist training file',
                        children: (<LoadExistFile getTrainingFileName={getTrainingFileName} research_id={research_id} />),
                    }
                ]}
            />
        </div>
    );
};
export default SegmentLabelSave;