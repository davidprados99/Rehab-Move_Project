--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4
-- Dumped by pg_dump version 16.4

-- Started on 2026-03-22 13:36:17

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 4 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- TOC entry 4968 (class 0 OID 0)
-- Dependencies: 4
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 16473)
-- Name: appointment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appointment (
    id_appointment integer NOT NULL,
    state character varying(50) DEFAULT 'pendiente'::character varying,
    date timestamp without time zone NOT NULL,
    notes text,
    id_patient integer,
    id_physio integer,
    CONSTRAINT appointment_state_check CHECK (((state)::text = ANY ((ARRAY['pendiente'::character varying, 'completado'::character varying, 'cancelado'::character varying])::text[])))
);


--
-- TOC entry 219 (class 1259 OID 16472)
-- Name: appointment_id_appointment_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.appointment_id_appointment_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4969 (class 0 OID 0)
-- Dependencies: 219
-- Name: appointment_id_appointment_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.appointment_id_appointment_seq OWNED BY public.appointment.id_appointment;


--
-- TOC entry 224 (class 1259 OID 16510)
-- Name: exercise; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise (
    id_exercise integer NOT NULL,
    name character varying(150) NOT NULL,
    description text,
    video_url character varying(255),
    active boolean DEFAULT true
);


--
-- TOC entry 226 (class 1259 OID 16520)
-- Name: exercise_assignment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise_assignment (
    id_assignment integer NOT NULL,
    weekly_frequency integer,
    series integer,
    repetitions integer,
    start_date date,
    end_date date,
    id_patient integer,
    id_exercise integer
);


--
-- TOC entry 225 (class 1259 OID 16519)
-- Name: exercise_assignment_id_assignment_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_assignment_id_assignment_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4970 (class 0 OID 0)
-- Dependencies: 225
-- Name: exercise_assignment_id_assignment_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_assignment_id_assignment_seq OWNED BY public.exercise_assignment.id_assignment;


--
-- TOC entry 228 (class 1259 OID 16542)
-- Name: exercise_done; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.exercise_done (
    id_done integer NOT NULL,
    done_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    id_assignment integer
);


--
-- TOC entry 227 (class 1259 OID 16541)
-- Name: exercise_done_id_done_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_done_id_done_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4971 (class 0 OID 0)
-- Dependencies: 227
-- Name: exercise_done_id_done_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_done_id_done_seq OWNED BY public.exercise_done.id_done;


--
-- TOC entry 223 (class 1259 OID 16509)
-- Name: exercise_id_exercise_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.exercise_id_exercise_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4972 (class 0 OID 0)
-- Dependencies: 223
-- Name: exercise_id_exercise_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.exercise_id_exercise_seq OWNED BY public.exercise.id_exercise;


--
-- TOC entry 222 (class 1259 OID 16494)
-- Name: pain_record; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pain_record (
    id_pain_record integer NOT NULL,
    level_pain integer,
    date date DEFAULT CURRENT_DATE,
    comment text,
    id_patient integer,
    CONSTRAINT pain_record_level_pain_check CHECK (((level_pain >= 0) AND (level_pain <= 10)))
);


--
-- TOC entry 221 (class 1259 OID 16493)
-- Name: pain_record_id_pain_record_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pain_record_id_pain_record_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4973 (class 0 OID 0)
-- Dependencies: 221
-- Name: pain_record_id_pain_record_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pain_record_id_pain_record_seq OWNED BY public.pain_record.id_pain_record;


--
-- TOC entry 218 (class 1259 OID 16456)
-- Name: patient; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.patient (
    id_patient integer NOT NULL,
    name character varying(100) NOT NULL,
    surnames character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    password character varying(255) NOT NULL,
    start_date date DEFAULT CURRENT_DATE,
    id_physio integer,
    role character varying(10) DEFAULT 'patient'::character varying
);


--
-- TOC entry 217 (class 1259 OID 16455)
-- Name: patient_id_patient_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.patient_id_patient_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4974 (class 0 OID 0)
-- Dependencies: 217
-- Name: patient_id_patient_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.patient_id_patient_seq OWNED BY public.patient.id_patient;


--
-- TOC entry 216 (class 1259 OID 16445)
-- Name: physio; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.physio (
    id_physio integer NOT NULL,
    name character varying(100) NOT NULL,
    surnames character varying(100) NOT NULL,
    email character varying(150) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying(10) DEFAULT 'physio'::character varying
);


--
-- TOC entry 215 (class 1259 OID 16444)
-- Name: physio_id_physio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.physio_id_physio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 4975 (class 0 OID 0)
-- Dependencies: 215
-- Name: physio_id_physio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.physio_id_physio_seq OWNED BY public.physio.id_physio;


--
-- TOC entry 4770 (class 2604 OID 16476)
-- Name: appointment id_appointment; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointment ALTER COLUMN id_appointment SET DEFAULT nextval('public.appointment_id_appointment_seq'::regclass);


--
-- TOC entry 4774 (class 2604 OID 16513)
-- Name: exercise id_exercise; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise ALTER COLUMN id_exercise SET DEFAULT nextval('public.exercise_id_exercise_seq'::regclass);


--
-- TOC entry 4776 (class 2604 OID 16523)
-- Name: exercise_assignment id_assignment; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_assignment ALTER COLUMN id_assignment SET DEFAULT nextval('public.exercise_assignment_id_assignment_seq'::regclass);


--
-- TOC entry 4777 (class 2604 OID 16545)
-- Name: exercise_done id_done; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_done ALTER COLUMN id_done SET DEFAULT nextval('public.exercise_done_id_done_seq'::regclass);


--
-- TOC entry 4772 (class 2604 OID 16497)
-- Name: pain_record id_pain_record; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pain_record ALTER COLUMN id_pain_record SET DEFAULT nextval('public.pain_record_id_pain_record_seq'::regclass);


--
-- TOC entry 4767 (class 2604 OID 16459)
-- Name: patient id_patient; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient ALTER COLUMN id_patient SET DEFAULT nextval('public.patient_id_patient_seq'::regclass);


--
-- TOC entry 4765 (class 2604 OID 16448)
-- Name: physio id_physio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.physio ALTER COLUMN id_physio SET DEFAULT nextval('public.physio_id_physio_seq'::regclass);


--
-- TOC entry 4954 (class 0 OID 16473)
-- Dependencies: 220
-- Data for Name: appointment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.appointment (id_appointment, state, date, notes, id_patient, id_physio) FROM stdin;
1	completado	2026-03-23 00:00:00		1	1
\.


--
-- TOC entry 4958 (class 0 OID 16510)
-- Dependencies: 224
-- Data for Name: exercise; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.exercise (id_exercise, name, description, video_url, active) FROM stdin;
1	Plancha abdominal	La plancha abdominal (plank) es un ejercicio isométrico fundamental para fortalecer el core, glúteos y hombros, manteniendo el cuerpo en línea recta apoyado sobre antebrazos y puntas de pies.	https://www.youtube.com/watch?v=zfY5XXa26ug	t
2	Puente glúteo	El puente de glúteo es un ejercicio de fuerza funcional que consiste en elevar la pelvis desde una posición tumbada boca arriba hasta que el cuerpo forma una línea recta desde los hombros hasta las rodillas.	https://www.youtube.com/watch?v=FJmXn7I6nwI	t
3	Rotación externa de hombro con banda elástica	La rotación externa de hombro con banda elástica es un ejercicio de fortalecimiento y estabilidad en el que el brazo gira hacia afuera, alejándose de la línea media del cuerpo, utilizando la resistencia de una banda para trabajar los músculos del manguito rotador.	https://www.youtube.com/watch?v=5xZkaSZlp8E	t
\.


--
-- TOC entry 4960 (class 0 OID 16520)
-- Dependencies: 226
-- Data for Name: exercise_assignment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.exercise_assignment (id_assignment, weekly_frequency, series, repetitions, start_date, end_date, id_patient, id_exercise) FROM stdin;
1	5	3	10	2026-03-22	2026-04-22	1	1
2	5	2	15	2026-03-22	2026-04-06	1	2
\.


--
-- TOC entry 4962 (class 0 OID 16542)
-- Dependencies: 228
-- Data for Name: exercise_done; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.exercise_done (id_done, done_date, id_assignment) FROM stdin;
1	2026-03-22 13:28:01.617485	1
\.


--
-- TOC entry 4956 (class 0 OID 16494)
-- Dependencies: 222
-- Data for Name: pain_record; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pain_record (id_pain_record, level_pain, date, comment, id_patient) FROM stdin;
1	6	2026-03-15	Siento una ligera presión en la zona lumbar al estar sentada.	1
\.


--
-- TOC entry 4952 (class 0 OID 16456)
-- Dependencies: 218
-- Data for Name: patient; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.patient (id_patient, name, surnames, email, password, start_date, id_physio, role) FROM stdin;
1	Lucía	Luque de la Casa	lucialuquetrad@gemail.com	pass21	2026-03-22	1	patient
2	Enrique	Maya Fernández	noharry@gemail.com	contraseña99	2026-03-15	1	patient
3	Iván	Rioja Marrero	danivan08@gemail.com	112299	2026-01-16	1	patient
4	Marta	Fernández García	martaFer@gemail.com	0055pass	2026-03-06	2	patient
\.


--
-- TOC entry 4950 (class 0 OID 16445)
-- Dependencies: 216
-- Data for Name: physio; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.physio (id_physio, name, surnames, email, password, role) FROM stdin;
1	David	Prados Medina	davidprados99@gemail.com	261199	physio
2	Sergio	Moreno García	sergiomoreno97@gemail.com	261197	physio
\.


--
-- TOC entry 4976 (class 0 OID 0)
-- Dependencies: 219
-- Name: appointment_id_appointment_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.appointment_id_appointment_seq', 1, true);


--
-- TOC entry 4977 (class 0 OID 0)
-- Dependencies: 225
-- Name: exercise_assignment_id_assignment_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exercise_assignment_id_assignment_seq', 2, true);


--
-- TOC entry 4978 (class 0 OID 0)
-- Dependencies: 227
-- Name: exercise_done_id_done_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exercise_done_id_done_seq', 1, true);


--
-- TOC entry 4979 (class 0 OID 0)
-- Dependencies: 223
-- Name: exercise_id_exercise_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.exercise_id_exercise_seq', 3, true);


--
-- TOC entry 4980 (class 0 OID 0)
-- Dependencies: 221
-- Name: pain_record_id_pain_record_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pain_record_id_pain_record_seq', 1, true);


--
-- TOC entry 4981 (class 0 OID 0)
-- Dependencies: 217
-- Name: patient_id_patient_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.patient_id_patient_seq', 4, true);


--
-- TOC entry 4982 (class 0 OID 0)
-- Dependencies: 215
-- Name: physio_id_physio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.physio_id_physio_seq', 2, true);


--
-- TOC entry 4790 (class 2606 OID 16482)
-- Name: appointment appointment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (id_appointment);


--
-- TOC entry 4796 (class 2606 OID 16525)
-- Name: exercise_assignment exercise_assignment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_assignment
    ADD CONSTRAINT exercise_assignment_pkey PRIMARY KEY (id_assignment);


--
-- TOC entry 4798 (class 2606 OID 16548)
-- Name: exercise_done exercise_done_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_done
    ADD CONSTRAINT exercise_done_pkey PRIMARY KEY (id_done);


--
-- TOC entry 4794 (class 2606 OID 16518)
-- Name: exercise exercise_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise
    ADD CONSTRAINT exercise_pkey PRIMARY KEY (id_exercise);


--
-- TOC entry 4792 (class 2606 OID 16503)
-- Name: pain_record pain_record_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pain_record
    ADD CONSTRAINT pain_record_pkey PRIMARY KEY (id_pain_record);


--
-- TOC entry 4786 (class 2606 OID 16466)
-- Name: patient patient_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_email_key UNIQUE (email);


--
-- TOC entry 4788 (class 2606 OID 16464)
-- Name: patient patient_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (id_patient);


--
-- TOC entry 4782 (class 2606 OID 16454)
-- Name: physio physio_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.physio
    ADD CONSTRAINT physio_email_key UNIQUE (email);


--
-- TOC entry 4784 (class 2606 OID 16452)
-- Name: physio physio_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.physio
    ADD CONSTRAINT physio_pkey PRIMARY KEY (id_physio);


--
-- TOC entry 4800 (class 2606 OID 16483)
-- Name: appointment appointment_id_patient_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_id_patient_fkey FOREIGN KEY (id_patient) REFERENCES public.patient(id_patient) ON DELETE CASCADE;


--
-- TOC entry 4801 (class 2606 OID 16488)
-- Name: appointment appointment_id_physio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_id_physio_fkey FOREIGN KEY (id_physio) REFERENCES public.physio(id_physio) ON DELETE CASCADE;


--
-- TOC entry 4803 (class 2606 OID 16561)
-- Name: exercise_assignment exercise_assignment_id_exercise_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_assignment
    ADD CONSTRAINT exercise_assignment_id_exercise_fkey FOREIGN KEY (id_exercise) REFERENCES public.exercise(id_exercise) ON DELETE CASCADE;


--
-- TOC entry 4804 (class 2606 OID 16556)
-- Name: exercise_assignment exercise_assignment_id_patient_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_assignment
    ADD CONSTRAINT exercise_assignment_id_patient_fkey FOREIGN KEY (id_patient) REFERENCES public.patient(id_patient) ON DELETE CASCADE;


--
-- TOC entry 4805 (class 2606 OID 16549)
-- Name: exercise_done exercise_done_id_assignment_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.exercise_done
    ADD CONSTRAINT exercise_done_id_assignment_fkey FOREIGN KEY (id_assignment) REFERENCES public.exercise_assignment(id_assignment) ON DELETE CASCADE;


--
-- TOC entry 4802 (class 2606 OID 16504)
-- Name: pain_record pain_record_id_patient_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pain_record
    ADD CONSTRAINT pain_record_id_patient_fkey FOREIGN KEY (id_patient) REFERENCES public.patient(id_patient) ON DELETE CASCADE;


--
-- TOC entry 4799 (class 2606 OID 16467)
-- Name: patient patient_id_physio_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.patient
    ADD CONSTRAINT patient_id_physio_fkey FOREIGN KEY (id_physio) REFERENCES public.physio(id_physio) ON DELETE SET NULL;


-- Completed on 2026-03-22 13:36:18

--
-- PostgreSQL database dump complete
--

