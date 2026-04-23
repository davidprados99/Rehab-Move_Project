interface ExerciseCardProps {
    name: string;
    description: string;
    video_url: string;
    isCompleted: boolean;
    onButtonClick?: () => void;
    className?: string;
}

const ExerciseCard: React.FC<ExerciseCardProps> = ({
    name,
    description,
    video_url,
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
        <div className={`bg-white rounded-rehab shadow-lg overflow-hidden flex flex-col w-full max-w-sm mx-auto border border-gray-100 ${className}`}>
            
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
                <h2 className="text-xl font-bold text-rehab-dark mb-2">{name}</h2>
                <p className="text-gray-600 line-clamp-3 md:line-clamp-none">{description}</p>
            </div>

            {/* Button container */}
            <div className="mt-4 flex justify-end items-center border-t pt-4">
                {isCompleted ? (
                    <span className="flex items-center text-green-600 text-sm font-semibold italic">¡Ejercicio hecho por hoy!</span>
                ) : (
                <button 
                onClick={onButtonClick}
                className="bg-rehab-primary hover:bg-rehab-primary/90 text-white text-xs font-bold px-4 py-2 rounded-lg transition-all shadow-md active:scale-95 uppercase tracking-wider">
                    Ejercicio hecho
                </button>
                )}
            </div>
        </div>
    );
}

export default ExerciseCard;
