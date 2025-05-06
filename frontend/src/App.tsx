import { Fragment, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { StyledDropzone } from "./components";
import { useDetectPlate } from "./hooks";

export default function App() {
  const { mutate, data: result } = useDetectPlate();

  // Handle dropped files
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        mutate(acceptedFiles[0]);
      }
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  // Initialize the dropzone hook
  const dropzoneState = useDropzone({
    accept: {
      "image/*": [".jpg", ".jpeg", ".png"],
    },
    maxFiles: 1,
    multiple: false,
    onDrop,
  });

  return (
    <div className="flex flex-col items-center gap-4 mt-8 h-screen">
      <h1 className="text-4xl font-bold">License Plate Detector</h1>

      <StyledDropzone {...dropzoneState} />

      {result && (
        <div className="flex flex-col items-center gap-4 w-[480px]">
          <img
            src={`data:image/jpeg;base64,${result.highlighted}`}
            alt="Highlighted"
            className="w-full"
          />
          {result.length ? (
            <div className="grid gap-4 grid-cols-2 place-items-center w-full">
              {Array.from({ length: result.length }).map((_, index) => {
                const img = result.cropped[index];
                const ocr = result.ocr[index];

                return (
                  <Fragment key={index}>
                    <img
                      src={`data:image/jpeg;base64,${img}`}
                      alt="Cropped Plate"
                      className="h-[60px]"
                    />
                    <div className="h-[60px] w-full bg-white border-2 rounded-lg flex overflow-hidden items-center">
                      <div className="h-full w-6 bg-blue-500"></div>
                      <p className="text-center flex-1 text-5xl">{ocr}</p>
                    </div>
                  </Fragment>
                );
              })}
            </div>
          ) : (
            <p className="text-2xl">No license plate detected</p>
          )}
        </div>
      )}
    </div>
  );
}
