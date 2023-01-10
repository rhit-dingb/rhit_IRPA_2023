import "./chatBot.css";
import React from "react";
import react, { useEffect, useState } from "react";
import { BiBot, BiUser } from "react-icons/bi";
import * as XLSX from 'xlsx';
import CUSTOM_BACKEND_API_STRING from "../constants/constants"


function UploadData() {

    const handleUpload = (file) => {
            const reader = new FileReader();
            reader.readAsArrayBuffer(file)
            reader.onload = () => {
            const result = reader.result
            const workbook = XLSX.read(result, { type: 'array' });

            let jsonData = {}
            for (let sheetName of workbook.SheetNames) {
                const sheet = workbook.Sheets[sheetName];
                jsonData[sheetName] = XLSX.utils.sheet_to_json(sheet);
            }
            //   jsonData = workbook.SheetNames.map((sheetName) => {
            //     const sheet = workbook.Sheets[sheetName];
            //     return XLSX.utils.sheet_to_json(sheet);
            //   });
            //   jsonData = JSON.stringify(jsonData)
            console.log(jsonData)
            fetch(CUSTOM_BACKEND_API_STRING+'/api/upload_cds_data', {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                'Content-Type': 'application/json'
                },
            });
        };
      }
    
  
    return (
        <div>
            <input type="file" accept=".xlsx" onChange={(e) => handleUpload(e.target.files[0])} />
        </div>
    )
}

export default UploadData
