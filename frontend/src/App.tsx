import { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import { StyledDropzone } from "./components";

export default function App() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{
    ocr: string[];
    highlighted: string;
    cropped: string[];
  } | null>(null);

  useEffect(() => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/detect", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setResult(data);
      });
  }, [file]);

  // Handle dropped files
  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFile(acceptedFiles[0]);
  }, []);

  // Initialize the dropzone hook
  const dropzoneState = useDropzone({
    accept: {
      "image/jpeg": [".jpeg", ".jpg"],
    },
    maxFiles: 1,
    onDrop,
    multiple: false,
  });

  return (
    <div className="flex flex-col items-center gap-8 mt-8 h-screen">
      <h1 className="text-4xl font-bold">License Plate Detector</h1>

      <StyledDropzone {...dropzoneState} />

      <pre>
        {result && (
          <div className="flex flex-col gap-4 items-center">
            <img
              src={`data:image/jpeg;base64,${result.highlighted}`}
              alt="Highlighted"
              className="w-[480px]"
            />
            <div className="flex w-full gap-4">
              <div className="grid gap-4 grid-cols-2">
                {result.cropped.map((item, index) => (
                  <img
                    key={index}
                    src={`data:image/jpeg;base64,${item}`}
                    alt="Cropped Plate"
                    className="col-span-1 col-start-1 w-full"
                  />
                ))}
                {result.ocr.map((item, index) => (
                  <div
                    key={index}
                    className="col-span-1 col-start-2 bg-white border-2 rounded-lg flex overflow-hidden items-center"
                  >
                    <div className="h-full w-6 bg-blue-500"></div>
                    <p className="text-center flex-1 text-5xl">{item}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </pre>
    </div>
  );
}
