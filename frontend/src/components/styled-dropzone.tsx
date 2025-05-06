import { useDropzone } from "react-dropzone";

type StyledDropzoneProps = ReturnType<typeof useDropzone>;

const ROOT_BASE_CLASS = `h-[80px] w-[480px]
border-2 border-dashed rounded-lg
bg-gray-100 border-gray-300"
transition-colors duration-300
flex items-center justify-center
cursor-pointer hover:bg-gray-200
`;
const ROOT_ACCEPT_CLASS = "border-green-500 bg-green-100";
const ROOT_REJECT_CLASS = "border-red-500 bg-red-100";

function StyledDropzone({
  getRootProps,
  getInputProps,
  isDragAccept,
  isDragReject,
  isDragActive,
}: StyledDropzoneProps) {
  return (
    <div
      {...getRootProps({
        className: `${ROOT_BASE_CLASS}
        ${isDragAccept ? ROOT_ACCEPT_CLASS : ""}
        ${isDragReject ? ROOT_REJECT_CLASS : ""}
        `,
      })}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <>
          {isDragAccept && <p>Drop the files here ...</p>}
          {isDragReject && <p>Unsupported file type...</p>}
        </>
      ) : (
        <p>Drag 'n' drop an image file here or click to select one</p>
      )}
    </div>
  );
}

export { StyledDropzone };

export type { StyledDropzoneProps };
