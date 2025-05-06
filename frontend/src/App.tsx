import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { StyledDropzone } from "./components";

export default function App() {
  const [file, setFile] = useState<File | null>(null);

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
        {file ? (
          // Display the image file name and size
          <>
            <img
              src={URL.createObjectURL(file)}
              alt="Preview"
              className="w-[480px]"
            />
          </>
        ) : null}
      </pre>
    </div>
  );
}
