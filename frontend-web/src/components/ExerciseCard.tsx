import React from 'react';
import tick from '../assets/tick.png';
import '../index.css';

interface ExerciseCardProps {
    name: string;
    description: string;
    video_url: string;
    isCompleted: boolean;
    onButtonClick?: () => void;
    className?: string;
    weekly_frequency: number;
    series: number;
    repetitions: number;
    start_date: string;
    end_date: string;
}

const ExerciseCard: React.FC<ExerciseCardProps> = ({
    name,
    description,
    video_url,
    weekly_frequency,
    series,
    repetitions,
    start_date,
    end_date,
    onButtonClick,
    isCompleted,
    className = "",
}) => {  
    // Function to convert various YouTube URL formats to embed format
    const getEmbedUrl = (url: string) => {
    if (!url) return "";
    
    // If the URL is already an embed link, return it as is
    if (url.includes("/embed/")) return url;

    // Case 1: YouTube Shorts (shorts/ID)
    if (url.includes("shorts/")) {
        return url.replace("shorts/", "embed/");
    }

    // Case 2: Standard YouTube (watch?v=ID)
    if (url.includes("watch?v=")) {
        return url.replace("watch?v=", "embed/");
    }

    // Case 3: YouTube short URL (youtu.be/ID)
    if (url.includes("youtu.be/")) {
        const id = url.split("/").pop();
        return `https://www.youtube.com/embed/${id}`;
    }

    return url;
};

    const embedUrl = getEmbedUrl(video_url);

    return (
        <div className={`bg-rehab-dark rounded-rehab shadow-lg overflow-hidden flex flex-col w-full max-w-sm mx-auto border border-gray-100 ${className}`}>
            
            {/* Video container */}
            <div className="w-full aspect-video bg-black">
                <iframe
                    src={embedUrl}
                    title={name}
                    className="w-full h-full"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                />
            </div>

            {/* Text container */}
            <div className="p-6 flex-1 flex flex-col">
                <h2 className="text-2xl text-center font-bold text-rehab-light mb-4">{name}</h2>
                <p className="text-rehab-light text-opacity-80 line-clamp-3 md:line-clamp-none">{description}</p>
            </div>
            {/* Details container */}
            <div className="px-6 py-4 border-t">
                <details>
                    <summary className="cursor-pointer text-rehab-light mb-2">Ver detalles</summary>
                    <p className="text-xs text-rehab-light mb-1"><span className="font-semibold">Frecuencia semanal:</span> {weekly_frequency}</p>
                    <p className="text-xs text-rehab-light mb-1"><span className="font-semibold">Series:</span> {series}</p>
                    <p className="text-xs text-rehab-light mb-1"><span className="font-semibold">Repeticiones:</span> {repetitions}</p>
                    <p className="text-xs text-rehab-light mb-1"><span className="font-semibold">Fecha de inicio:</span> {new Date(start_date).toLocaleDateString()}</p>
                    <p className="text-xs text-rehab-light"><span className="font-semibold">Fecha de fin:</span> {new Date(end_date).toLocaleDateString()}</p>
                </details>
            </div>

            {/* Button container */}
            <div className="mt-4 flex justify-center items-center border-t pt-4 mb-4">
                {isCompleted ? (
                    <span className="flex items-center text-rehab-light text-sm font-semibold italic">
                        ¡Ejercicio hecho por hoy! <img src={tick} alt="Checkmark" className="ml-2 w-4 h-4 rounded-full overflow-hidden bg-green-500" /> 
                        </span>
                ) : (
                <button 
                onClick={onButtonClick}
                className="bg-rehab-primary hover:bg-rehab-primary/90 text-white text-xs font-bold px-4 py-2 rounded-lg transition-all shadow-md active:scale-95  tracking-wider">
                    Pulsa cuando termines
                </button>
                )}
            </div>
        </div>
    );
}

export default ExerciseCard;
