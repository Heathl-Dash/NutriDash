--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg120+1)
-- Dumped by pg_dump version 17.5 (Debian 17.5-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: habits; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.habits (
    habit_id integer NOT NULL,
    title character varying NOT NULL,
    description character varying NOT NULL,
    positive boolean,
    negative boolean,
    positive_count integer,
    negative_count integer,
    user_id integer NOT NULL,
    created timestamp without time zone NOT NULL
);


ALTER TABLE public.habits OWNER TO postgres;

--
-- Name: habits_habit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.habits_habit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.habits_habit_id_seq OWNER TO postgres;

--
-- Name: habits_habit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.habits_habit_id_seq OWNED BY public.habits.habit_id;


--
-- Name: to_do_histories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.to_do_histories (
    to_do_history_id integer NOT NULL,
    todo_id integer NOT NULL,
    date_done date
);


ALTER TABLE public.to_do_histories OWNER TO postgres;

--
-- Name: to_do_histories_to_do_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.to_do_histories_to_do_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.to_do_histories_to_do_history_id_seq OWNER TO postgres;

--
-- Name: to_do_histories_to_do_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.to_do_histories_to_do_history_id_seq OWNED BY public.to_do_histories.to_do_history_id;


--
-- Name: to_dos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.to_dos (
    todo_id integer NOT NULL,
    title character varying NOT NULL,
    description character varying NOT NULL,
    done boolean,
    user_id integer NOT NULL,
    created timestamp without time zone NOT NULL
);


ALTER TABLE public.to_dos OWNER TO postgres;

--
-- Name: to_dos_todo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.to_dos_todo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.to_dos_todo_id_seq OWNER TO postgres;

--
-- Name: to_dos_todo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.to_dos_todo_id_seq OWNED BY public.to_dos.todo_id;


--
-- Name: water_bottles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.water_bottles (
    water_bottle_id integer NOT NULL,
    water_goal_id integer NOT NULL,
    bottle_name character varying NOT NULL,
    ml_bottle integer NOT NULL,
    user_id integer NOT NULL,
    id_bottle_style integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.water_bottles OWNER TO postgres;

--
-- Name: water_bottles_water_bottle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.water_bottles_water_bottle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.water_bottles_water_bottle_id_seq OWNER TO postgres;

--
-- Name: water_bottles_water_bottle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.water_bottles_water_bottle_id_seq OWNED BY public.water_bottles.water_bottle_id;


--
-- Name: water_goal_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.water_goal_logs (
    id integer NOT NULL,
    action character varying NOT NULL,
    water_goal_id integer NOT NULL,
    user_id integer,
    old_data json,
    new_data json,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.water_goal_logs OWNER TO postgres;

--
-- Name: water_goal_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.water_goal_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.water_goal_logs_id_seq OWNER TO postgres;

--
-- Name: water_goal_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.water_goal_logs_id_seq OWNED BY public.water_goal_logs.id;


--
-- Name: water_goals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.water_goals (
    water_goal_id integer NOT NULL,
    ml_goal integer NOT NULL,
    ml_drinked integer,
    user_id integer NOT NULL,
    last_updated timestamp without time zone NOT NULL
);


ALTER TABLE public.water_goals OWNER TO postgres;

--
-- Name: water_goals_water_goal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.water_goals_water_goal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.water_goals_water_goal_id_seq OWNER TO postgres;

--
-- Name: water_goals_water_goal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.water_goals_water_goal_id_seq OWNED BY public.water_goals.water_goal_id;


--
-- Name: habits habit_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habits ALTER COLUMN habit_id SET DEFAULT nextval('public.habits_habit_id_seq'::regclass);


--
-- Name: to_do_histories to_do_history_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.to_do_histories ALTER COLUMN to_do_history_id SET DEFAULT nextval('public.to_do_histories_to_do_history_id_seq'::regclass);


--
-- Name: to_dos todo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.to_dos ALTER COLUMN todo_id SET DEFAULT nextval('public.to_dos_todo_id_seq'::regclass);


--
-- Name: water_bottles water_bottle_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_bottles ALTER COLUMN water_bottle_id SET DEFAULT nextval('public.water_bottles_water_bottle_id_seq'::regclass);


--
-- Name: water_goal_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_goal_logs ALTER COLUMN id SET DEFAULT nextval('public.water_goal_logs_id_seq'::regclass);


--
-- Name: water_goals water_goal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_goals ALTER COLUMN water_goal_id SET DEFAULT nextval('public.water_goals_water_goal_id_seq'::regclass);


--
-- Data for Name: habits; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.habits (habit_id, title, description, positive, negative, positive_count, negative_count, user_id, created) FROM stdin;
\.


--
-- Data for Name: to_do_histories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.to_do_histories (to_do_history_id, todo_id, date_done) FROM stdin;
\.


--
-- Data for Name: to_dos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.to_dos (todo_id, title, description, done, user_id, created) FROM stdin;
\.


--
-- Data for Name: water_bottles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.water_bottles (water_bottle_id, water_goal_id, bottle_name, ml_bottle, user_id, id_bottle_style) FROM stdin;
1	3	garrafa 1	500	3	2
\.


--
-- Data for Name: water_goal_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.water_goal_logs (id, action, water_goal_id, user_id, old_data, new_data, "timestamp") FROM stdin;
1	create	3	3	null	{"water_goal_id": 3, "ml_goal": 2380, "ml_drinked": 0, "user_id": 3, "last_updated": "2025-07-09T21:19:02.083409"}	2025-07-09 21:19:02.08733
\.


--
-- Data for Name: water_goals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.water_goals (water_goal_id, ml_goal, ml_drinked, user_id, last_updated) FROM stdin;
3	2380	0	3	2025-07-09 21:19:02.083409
\.


--
-- Name: habits_habit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.habits_habit_id_seq', 1, false);


--
-- Name: to_do_histories_to_do_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.to_do_histories_to_do_history_id_seq', 1, false);


--
-- Name: to_dos_todo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.to_dos_todo_id_seq', 1, false);


--
-- Name: water_bottles_water_bottle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.water_bottles_water_bottle_id_seq', 1, true);


--
-- Name: water_goal_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.water_goal_logs_id_seq', 1, true);


--
-- Name: water_goals_water_goal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.water_goals_water_goal_id_seq', 3, true);


--
-- Name: habits habits_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.habits
    ADD CONSTRAINT habits_pkey PRIMARY KEY (habit_id);


--
-- Name: to_do_histories to_do_histories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.to_do_histories
    ADD CONSTRAINT to_do_histories_pkey PRIMARY KEY (to_do_history_id);


--
-- Name: to_dos to_dos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.to_dos
    ADD CONSTRAINT to_dos_pkey PRIMARY KEY (todo_id);


--
-- Name: water_bottles water_bottles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_bottles
    ADD CONSTRAINT water_bottles_pkey PRIMARY KEY (water_bottle_id);


--
-- Name: water_goal_logs water_goal_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_goal_logs
    ADD CONSTRAINT water_goal_logs_pkey PRIMARY KEY (id);


--
-- Name: water_goals water_goals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_goals
    ADD CONSTRAINT water_goals_pkey PRIMARY KEY (water_goal_id);


--
-- Name: ix_habits_habit_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_habits_habit_id ON public.habits USING btree (habit_id);


--
-- Name: ix_to_do_histories_to_do_history_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_to_do_histories_to_do_history_id ON public.to_do_histories USING btree (to_do_history_id);


--
-- Name: ix_to_dos_todo_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_to_dos_todo_id ON public.to_dos USING btree (todo_id);


--
-- Name: ix_water_bottles_water_bottle_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_water_bottles_water_bottle_id ON public.water_bottles USING btree (water_bottle_id);


--
-- Name: ix_water_goal_logs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_water_goal_logs_id ON public.water_goal_logs USING btree (id);


--
-- Name: ix_water_goals_water_goal_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_water_goals_water_goal_id ON public.water_goals USING btree (water_goal_id);


--
-- Name: to_do_histories to_do_histories_todo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.to_do_histories
    ADD CONSTRAINT to_do_histories_todo_id_fkey FOREIGN KEY (todo_id) REFERENCES public.to_dos(todo_id);


--
-- Name: water_bottles water_bottles_water_goal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.water_bottles
    ADD CONSTRAINT water_bottles_water_goal_id_fkey FOREIGN KEY (water_goal_id) REFERENCES public.water_goals(water_goal_id);


--
-- PostgreSQL database dump complete
--

