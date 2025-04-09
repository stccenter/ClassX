export default function useConvertObjToArr(obj) {
    let newArr = [];
    Object.keys(obj).map((key) => { newArr[key] = obj[key] })
    return newArr;
}