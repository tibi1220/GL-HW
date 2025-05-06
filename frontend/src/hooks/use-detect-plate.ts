import { useMutation } from "@tanstack/react-query";

function useDetectPlate() {
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/detect", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        return null;
      }

      return response.json() as Promise<{
        highlighted: string;
        ocr: string[];
        cropped: string[];
        length: number;
      }>;
    },
  });
}

export { useDetectPlate };
