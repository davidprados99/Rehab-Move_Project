const RehabLoader = () => (
    <div className="mt-30 flex flex-col items-center justify-center py-12">
        <div className="relative flex items-center justify-center">

            <div className="absolute animate-ping h-12 w-12 rounded-full bg-rehab-primary opacity-20"></div>
            <div className="absolute animate-pulse h-8 w-8 rounded-full bg-rehab-primary opacity-40"></div>
            <div className="relative h-4 w-4 rounded-full bg-rehab-primary"></div>

        </div>
        <p className="mt-8 text-sm font-medium text-rehab-primary animate-pulse tracking-widest uppercase">
            Cargando...
        </p>
    </div>
);

export default RehabLoader;